# QP Watch V13 - Quick Start Guide

Get your QP Watch up and running in 5 easy steps!

## 📋 Prerequisites

Before you begin, make sure you have:
- [ ] Arduino Nano (or compatible board)
- [ ] SSD1306 OLED Display (128x64, I2C)
- [ ] DS3231 RTC Module
- [ ] 3x Tactile Push Buttons
- [ ] Breadboard and jumper wires
- [ ] USB cable for programming
- [ ] Computer with Arduino IDE installed

## 🚀 Step 1: Install Arduino IDE

1. Download Arduino IDE from: https://www.arduino.cc/en/software
2. Install for your operating system (Windows, Mac, or Linux)
3. Launch Arduino IDE

## 📚 Step 2: Install Required Libraries

1. Open Arduino IDE
2. Go to: **Sketch → Include Library → Manage Libraries**
3. Search and install each of these libraries:

   - **Adafruit GFX Library** (by Adafruit)
   - **Adafruit SSD1306** (by Adafruit)
   - **RTClib** (by Adafruit)

4. Click "Install all" when prompted for dependencies

## 🔌 Step 3: Connect Hardware

### Wiring Diagram

```
Arduino Nano → Components

Power & I2C Bus:
5V     →  OLED VCC, RTC VCC
GND    →  OLED GND, RTC GND, All button terminals
A4     →  OLED SDA, RTC SDA
A5     →  OLED SCL, RTC SCL

Buttons:
D2     →  UP Button (other pin to GND)
D3     →  DOWN Button (other pin to GND)
D4     →  SELECT Button (other pin to GND)

Optional:
A0     →  Battery voltage divider (see hardware guide)
```

### Quick Connection Guide

**OLED Display:**
| OLED Pin | Arduino Pin |
|----------|-------------|
| VCC      | 5V          |
| GND      | GND         |
| SDA      | A4          |
| SCL      | A5          |

**DS3231 RTC:**
| RTC Pin  | Arduino Pin |
|----------|-------------|
| VCC      | 5V          |
| GND      | GND         |
| SDA      | A4 (shared) |
| SCL      | A5 (shared) |

**Buttons:**
| Button   | Arduino Pin | Other Pin |
|----------|-------------|-----------|
| UP       | D2          | GND       |
| DOWN     | D3          | GND       |
| SELECT   | D4          | GND       |

## 💻 Step 4: Upload the Code

1. **Download the code**:
   - Clone or download this repository
   - Or copy `QP_WATCH_V13.ino` to your computer

2. **Open the sketch**:
   - Double-click `QP_WATCH_V13.ino`
   - Arduino IDE will open

3. **Select your board**:
   - Go to: **Tools → Board → Arduino AVR Boards → Arduino Nano**

4. **Select processor** (if using Nano):
   - Go to: **Tools → Processor → ATmega328P (Old Bootloader)**
   - Try "ATmega328P" if old bootloader doesn't work

5. **Select port**:
   - Go to: **Tools → Port → [Select your Arduino's COM port]**
   - On Windows: COM3, COM4, etc.
   - On Mac/Linux: /dev/cu.usbserial or /dev/ttyUSB0

6. **Upload**:
   - Click the **Upload** button (→ icon)
   - Wait for "Done uploading" message

## ✅ Step 5: Test and Use

### First Boot

1. After upload completes, the watch should display:
   ```
   QP WATCH
   Version 13
   Improved Ed.
   ```

2. After 2 seconds, it will show the digital watchface

### Basic Controls

**From Watchface:**
- **UP button**: Open menu
- **DOWN button**: Change watchface style (Digital → Analog → Minimal)

**In Menu:**
- **UP/DOWN buttons**: Navigate menu items
- **SELECT button**: Choose highlighted item

**From any screen:**
- **SELECT button**: Return to menu (except watchface)

### Menu Options

1. **Watchface**: Return to main time display
2. **Steps**: View step counter and daily progress
3. **Heart Rate**: View heart rate (simulated)
4. **Battery**: Check battery level
5. **Settings**: View configuration options
6. **Sleep**: Manually enter sleep mode

### Troubleshooting First Boot

**Display shows nothing:**
- Check I2C connections (SDA, SCL)
- Verify display power (VCC, GND)
- Try address 0x3D in code if 0x3C doesn't work

**"RTC Error" message:**
- Check RTC connections
- Ensure RTC has backup battery (CR2032)
- Verify I2C address (should be 0x68)

**Compilation errors:**
- Ensure all libraries are installed
- Check Arduino IDE version (need 1.8.0 or newer)
- Verify board selection

**Upload fails:**
- Check USB cable (must support data, not just power)
- Try different COM port
- Press reset button on Arduino before upload
- Try "Old Bootloader" processor option

## 📖 Next Steps

### Set the Correct Time

The RTC automatically sets to compile time on first boot. To set custom time:

1. In Arduino IDE, modify this line in `setup()`:
   ```cpp
   // rtc.adjust(DateTime(2026, 2, 11, 14, 30, 0));
   ```

2. Uncomment and change to your desired time:
   ```cpp
   rtc.adjust(DateTime(2026, 2, 11, 14, 30, 0));
   // Format: (year, month, day, hour, minute, second)
   ```

3. Upload again
4. Re-comment the line and upload once more

### Customize Your Watch

Check out:
- **examples/configuration_example.ino** - Configuration options
- **docs/API_REFERENCE.md** - Function documentation
- **docs/HARDWARE_GUIDE.md** - Advanced hardware setup

### Add Optional Features

**For accurate step counting:**
- Add MPU6050 accelerometer (see Hardware Guide)

**For heart rate monitoring:**
- Add MAX30102 sensor (see Hardware Guide)

**For battery monitoring:**
- Build voltage divider circuit (see Hardware Guide)

## 🎯 Usage Tips

### Battery Life
- Enable auto-sleep for maximum battery life
- Reduce brightness in settings
- Sleep mode activates after 30 seconds of inactivity

### Button Tips
- Buttons use internal pull-ups (no external resistors needed)
- If buttons feel unresponsive, check ground connections
- Debouncing is built-in (200ms)

### Display Care
- OLED displays can suffer burn-in
- Use auto-sleep to extend display life
- Avoid showing static images for extended periods

## 📞 Getting Help

### Common Questions

**Q: Can I use Arduino Uno instead of Nano?**
A: Yes! Pin mappings are the same.

**Q: Display is upside down?**
A: Rotate the display physically or add rotation code.

**Q: Time is wrong?**
A: Follow "Set the Correct Time" section above.

**Q: Step counter not working?**
A: Currently simulated. Add MPU6050 for real tracking.

### Resources

- **Full Documentation**: README.md
- **Hardware Guide**: docs/HARDWARE_GUIDE.md
- **API Reference**: docs/API_REFERENCE.md
- **GitHub Issues**: https://github.com/b4-i-die/QP_WATCH_V001/issues

### Community Support

- Open an issue on GitHub for bugs
- Check existing issues for solutions
- Share your builds and modifications!

## 🎉 You're Ready!

Your QP Watch V13 is now running! Enjoy your new smartwatch!

**What's Next?**
- Customize the watchfaces
- Add sensors for real tracking
- Design a 3D printed case
- Share your modifications with the community

---

**Happy Making! ⌚✨**

QP WATCH V13 - Akıllı, Verimli, Gelişmiş (Smart, Efficient, Advanced)
