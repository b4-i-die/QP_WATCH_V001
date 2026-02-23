from fastapi import FastAPI, Request
import requests
from bs4 import BeautifulSoup
import uvicorn
import os

app = FastAPI()

# Telegram Bot Bilgileri (Render.com Environment Variables'dan alınacak)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "BURAYA_BOT_TOKEN_GELECEK")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "BURAYA_CHAT_ID_GELECEK")

def check_fundamentals(symbol: str):
    """
    İş Yatırım üzerinden hissenin temel verilerini (PD/DD ve F/K) çeker.
    Yahoo Finance botları engellediği için alternatif olarak kullanıyoruz.
    """
    try:
        # BIST:THYAO formatından sadece THYAO kısmını al
        clean_symbol = symbol.replace("BIST:", "").strip()
        
        # İş Yatırım hisse detay sayfası
        url = f"https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={clean_symbol}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # İş Yatırım sayfasındaki PD/DD ve F/K değerlerini bulma
        # Tablodaki değerleri bulmak için spesifik etiketleri arıyoruz
        pb_ratio = 999.0
        pe_ratio = 999.0
        
        # PD/DD (Piyasa Değeri / Defter Değeri)
        pd_dd_row = soup.find('td', string='PD/DD')
        if pd_dd_row and pd_dd_row.find_next_sibling('td'):
            val_str = pd_dd_row.find_next_sibling('td').text.strip().replace(',', '.')
            if val_str and val_str != '-':
                pb_ratio = float(val_str)
                
        # F/K (Fiyat / Kazanç)
        fk_row = soup.find('td', string='F/K')
        if fk_row and fk_row.find_next_sibling('td'):
            val_str = fk_row.find_next_sibling('td').text.strip().replace(',', '.')
            if val_str and val_str != '-':
                pe_ratio = float(val_str)
        
        print(f"İş Yatırım'dan çekilen veriler - {clean_symbol}: PD/DD={pb_ratio}, F/K={pe_ratio}")
        
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
