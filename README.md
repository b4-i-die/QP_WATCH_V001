# QP WATCH V13 - İyileştirilmiş Sürüm (Improved Version)

![Version](https://img.shields.io/badge/version-13.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Arduino](https://img.shields.io/badge/platform-Arduino-teal)

Advanced Arduino-based smartwatch with event-driven architecture and modern features.

## 🌟 Features

### V13 İyileştirmeleri (V13 Improvements)

- **🎨 Multiple Watchfaces**: Three different display styles
  - Digital watchface with full date/time
  - Analog watchface with classic clock hands
  - Minimal watchface for clean design
  
- **⚡ Event-Driven Architecture**: Efficient state machine implementation
  - Low power consumption
  - Fast response times
  - Smooth transitions between states

- **📊 Advanced Monitoring**
  - Real-time clock (RTC DS3231)
  - Step counter with activity tracking
  - Heart rate monitoring support
  - Battery level monitoring
  - 10,000 step daily goal tracking

- **💾 Power Management**
  - Auto-sleep mode after 30 seconds of inactivity
  - Configurable brightness settings
  - Battery-efficient display updates

- **🎛️ Customizable Settings**
  - Adjustable brightness
  - Auto-sleep toggle
  - Step tracking enable/disable
  - Multiple menu options

- **📱 User Interface**
  - Intuitive 3-button navigation
  - Responsive menu system
  - Visual feedback and animations
  - Progress bars and indicators

## 🔧 Hardware Requirements

### Minimum Components

- **Microcontroller**: Arduino Nano, Uno, or compatible (ATmega328P)
- **Display**: SSD1306 OLED (128x64, I2C)
- **Real-Time Clock**: DS3231 RTC module
- **Buttons**: 3x tactile push buttons
- **Battery**: 3.7V LiPo battery (500-1000mAh recommended)
- **Optional**: MPU6050 accelerometer for accurate step counting
- **Optional**: MAX30102 heart rate sensor

### Pin Connections

```
Component          | Arduino Pin
-------------------|-------------
OLED SDA          | A4 (SDA)
OLED SCL          | A5 (SCL)
DS3231 SDA        | A4 (SDA)
DS3231 SCL        | A5 (SCL)
Button UP         | D2
Button DOWN       | D3
Button SELECT     | D4
Battery Monitor   | A0
LED Indicator     | D13
```

## 📦 Software Dependencies

### Required Libraries

Install these libraries through Arduino Library Manager:

```
- Adafruit GFX Library (>= 1.11.0)
- Adafruit SSD1306 (>= 2.5.0)
- RTClib (>= 2.1.0)
- Wire (built-in)
```

### Installation Steps

1. **Install Arduino IDE** (version 1.8.x or 2.x)
   - Download from: https://www.arduino.cc/en/software

2. **Install Required Libraries**
   ```
   Sketch → Include Library → Manage Libraries
   Search and install:
   - Adafruit GFX
   - Adafruit SSD1306
   - RTClib
   ```

3. **Clone or Download This Repository**
   ```bash
   git clone https://github.com/b4-i-die/QP_WATCH_V001.git
   cd QP_WATCH_V001
   ```

4. **Open the Sketch**
   - Open `QP_WATCH_V13.ino` in Arduino IDE

5. **Select Board and Port**
   ```
   Tools → Board → Arduino Nano (or your board)
   Tools → Port → [Your COM Port]
   ```

6. **Upload to Arduino**
   - Click Upload button or press Ctrl+U

## 🎮 Usage Guide

### Button Controls

| Button | Function in Watchface | Function in Menu |
|--------|----------------------|------------------|
| UP     | Open menu           | Navigate up      |
| DOWN   | Change watchface style | Navigate down  |
| SELECT | -                   | Select item      |

### Navigation

1. **From Watchface**:
   - Press UP to enter menu
   - Press DOWN to cycle through watchface styles

2. **In Menu**:
   - Press UP/DOWN to navigate
   - Press SELECT to choose an option
   - SELECT from submenu returns to menu

3. **Menu Options**:
   - **Watchface**: Return to main watch display
   - **Steps**: View step count and daily goal progress
   - **Heart Rate**: View heart rate (simulated or from sensor)
   - **Battery**: Check battery level and status
   - **Settings**: Adjust watch preferences
   - **Sleep**: Enter sleep mode manually

### Watchface Styles

1. **Digital** (Default)
   - Shows time with HH:MM:SS format
   - Displays full date (DD/MM/YYYY)
   - Battery indicator in corner

2. **Analog**
   - Classic clock face with hour/minute hands
   - 12-hour marks around the circle
   - Clean, traditional design

3. **Minimal**
   - Large time display (HH:MM only)
   - Day of week indicator
   - Minimalist aesthetic

## 🔋 Power Management

### Battery Life Optimization

- **Auto-Sleep**: Screen turns off after 30 seconds of inactivity
- **Wake Up**: Press any button to wake from sleep
- **Low Power**: Display updates at optimal intervals
- **RTC**: DS3231 keeps time during sleep with minimal power

### Battery Monitoring

The watch continuously monitors battery level through analog pin A0. Connect battery voltage through a voltage divider:

```
Battery(+) ──[10kΩ]── A0 ──[10kΩ]── GND
```

## 🛠️ Customization

### Changing Step Goal

Edit in `displaySteps()` function:
```cpp
int goalSteps = 10000; // Change to your desired goal
```

### Adjusting Sleep Timeout

Edit at the top of the code:
```cpp
const unsigned long SLEEP_TIMEOUT = 30000; // milliseconds
```

### Adding Custom Watchfaces

1. Add new enum value to `WatchfaceStyle`
2. Create new `displayCustomWatchface()` function
3. Add case to switch statement in `displayWatchface()`

### Configuring RTC Time

The RTC is automatically set to compile time on first run. To manually set:

```cpp
// In setup(), add:
rtc.adjust(DateTime(2026, 2, 11, 12, 30, 0));
// Format: (year, month, day, hour, minute, second)
```

## 📊 State Machine

The watch uses an event-driven state machine architecture:

```
┌─────────────┐
│ WATCHFACE   │◄─── Default State
└──────┬──────┘
       │ UP Button
       ▼
┌─────────────┐
│    MENU     │◄─── Navigation Hub
└──────┬──────┘
       │ SELECT
       ├──────────► STEPS
       ├──────────► HEART_RATE
       ├──────────► BATTERY
       ├──────────► SETTINGS
       └──────────► SLEEP
```

## 🐛 Troubleshooting

### Display Not Working

- Check I2C connections (SDA/SCL)
- Verify display address (default: 0x3C)
- Test with I2C scanner sketch
- Check power supply (3.3V or 5V depending on module)

### RTC Not Keeping Time

- Replace CR2032 battery in DS3231 module
- Check I2C connections
- Verify RTC is properly initialized

### Buttons Not Responding

- Check pull-up resistors (internal pull-ups enabled in code)
- Verify button connections to correct pins
- Test with multimeter in continuity mode

### Compilation Errors

- Ensure all libraries are installed
- Update to latest library versions
- Check board selection matches your hardware
- Verify Arduino IDE version compatibility

## 🔄 Version History

### V13.0 (Current - İyileştirilmiş Sürüm)
- ✨ Three different watchface styles
- 📊 Enhanced step tracking with progress bar
- ❤️ Heart rate monitoring integration
- 🔋 Improved battery monitoring
- 💤 Auto-sleep power management
- 🎨 Better UI/UX with visual feedback
- ⚡ Optimized state machine implementation
- 📱 Comprehensive settings menu

### Earlier Versions
- V1-12: Development iterations and prototypes

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Guidelines

1. Follow existing code style
2. Comment your code clearly
3. Test thoroughly before submitting
4. Update documentation as needed

## 📧 Contact & Support

- **Author**: QP Watch Team
- **Repository**: https://github.com/b4-i-die/QP_WATCH_V001
- **Issues**: https://github.com/b4-i-die/QP_WATCH_V001/issues

## 🙏 Acknowledgments

- Adafruit for excellent Arduino libraries
- RTClib contributors
- Arduino community

## 🔮 Future Enhancements

Planned features for upcoming versions:

- [ ] Bluetooth connectivity for notifications
- [ ] GPS tracking support
- [ ] Weather display integration
- [ ] Customizable widgets
- [ ] Sleep quality monitoring
- [ ] Alarm and timer functions
- [ ] Activity auto-detection
- [ ] Multi-language support

---

**QP WATCH V13** - Akıllı, Verimli, Gelişmiş (Smart, Efficient, Advanced)

Made with ❤️ for the maker community