from fastapi import FastAPI, Request
import yfinance as yf
import requests
import uvicorn
import os

app = FastAPI()

# Telegram Bot Bilgileri (Render.com Environment Variables'dan alınacak)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "BURAYA_BOT_TOKEN_GELECEK")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "BURAYA_CHAT_ID_GELECEK")

def check_fundamentals(symbol: str):
    """
    Yahoo Finance üzerinden hissenin temel verilerini çeker.
    BIST hisseleri yfinance'ta .IS uzantısı ile bulunur (Örn: THYAO.IS)
    """
    try:
        yf_symbol = symbol.replace("BIST:", "") + ".IS"
        stock = yf.Ticker(yf_symbol)
        info = stock.info
        
        # Temel verileri çek (Bulunamazsa 999 ata ki filtreye takılsın)
        pb_ratio = info.get('priceToBook', 999) # PD/DD
        pe_ratio = info.get('trailingPE', 999)  # F/K
        
        # Kriterler: PD/DD < 2.0 VE F/K < 10.0
        is_attractive = (pb_ratio < 2.0) and (pe_ratio < 10.0)
        
        return is_attractive, pb_ratio, pe_ratio
    except Exception as e:
        print(f"Hata oluştu ({symbol}): {e}")
        return False, 999, 999

def send_telegram_message(text: str):
    """Telegram'a mesaj gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.post("/webhook")
async def receive_webhook(request: Request):
    """TradingView'dan gelen JSON sinyalini karşılar."""
    data = await request.json()
    symbol = data.get("symbol")
    signal = data.get("signal")
    price = data.get("price")
    
    print(f"Sinyal Alındı: {symbol} - {signal} - {price} TL")
    
    # 1. Temel Analiz Kontrolü
    is_attractive, pb, pe = check_fundamentals(symbol)
    
    # 2. Eğer cazipse Telegram'a gönder
    if is_attractive:
        msg = f"🚨 **YENİ CAZİP HİSSE TESPİTİ** 🚨\n\n"
        msg += f"📌 **Hisse:** {symbol}\n"
        msg += f"⚙️ **Teknik Sinyal:** {signal} (V404 Onaylı)\n"
        msg += f"💰 **Anlık Fiyat:** {price} TL\n\n"
        msg += f"📊 **Temel Veriler:**\n"
        msg += f"• PD/DD: {pb:.2f} (Kriter: < 2.0)\n"
        msg += f"• F/K: {pe:.2f} (Kriter: < 10.0)\n\n"
        msg += f"✅ *Hem teknik hem temel olarak yatırıma uygundur.*"
        
        send_telegram_message(msg)
        return {"status": "success", "message": "Sent to Telegram"}
    else:
        print(f"Filtreye Takıldı: {symbol} (PD/DD: {pb}, F/K: {pe})")
        return {"status": "ignored", "message": "Fundamentals not attractive"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
