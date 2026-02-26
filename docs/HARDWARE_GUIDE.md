# QP Watch V13 - Hardware Assembly Guide

## Bill of Materials (BOM)

### Essential Components

| Component | Quantity | Specifications | Estimated Price |
|-----------|----------|----------------|-----------------|
| Arduino Nano | 1 | ATmega328P, 5V/16MHz | $3-5 |
| SSD1306 OLED | 1 | 128x64, I2C, 0.96" | $3-5 |
| DS3231 RTC | 1 | I2C, with battery backup | $2-4 |
| Tactile Buttons | 3 | 6x6mm, through-hole | $0.50 |
| LiPo Battery | 1 | 3.7V, 500-1000mAh | $5-8 |
| Battery Charger | 1 | TP4056 module | $1-2 |
| Resistors | 2 | 10kΩ, 1/4W | $0.10 |
| PCB/Breadboard | 1 | Custom or prototype board | $2-5 |
| Wires | - | Jumper wires or solid core | $1-2 |

### Optional Components

| Component | Quantity | Specifications | Purpose |
|-----------|----------|----------------|---------|
| MPU6050 | 1 | 6-axis accelerometer/gyro | Accurate step counting |
| MAX30102 | 1 | Heart rate/SpO2 sensor | Heart rate monitoring |
| Buzzer | 1 | Passive 5V buzzer | Notifications/alarms |
| Vibration Motor | 1 | 3V coin motor | Haptic feedback |
| 3D Printed Case | 1 | Custom design | Enclosure |

**Total Estimated Cost**: $20-35 (basic version)

## Circuit Diagram

### Basic Schematic

```
                    ┌─────────────────┐
                    │  Arduino Nano   │
                    │                 │
    ┌───────────────┤ A4 (SDA)        │
    │           ┌───┤ A5 (SCL)        │
    │           │   │                 │
    │           │   │ D2 ├────┐       │
    │           │   │ D3 ├────┼───┐   │
    │           │   │ D4 ├────┼───┼───┐
    │           │   │    │    │   │   │
    │           │   │ A0 ├────┤   │   │
    │           │   │    │    │   │   │
    │           │   │ D13├──►LED   │   │
    │           │   │    │        │   │
    │           │   │ VIN├─ Battery  │   │
    │           │   │ GND├─ ┴     │   │
    │           │   └────┴────┘   │   │
    │           │                 │   │
    ▼           ▼                 ▼   ▼
┌────────┐  ┌────────┐      ┌─────┐┌─────┐
│SSD1306 │  │DS3231  │      │ UP  ││DOWN │
│  OLED  │  │  RTC   │      │ BTN ││ BTN │
│        │  │        │      └──┬──┘└──┬──┘
│ SDA SCL│  │ SDA SCL│         │      │
└─┬───┬──┘  └─┬───┬──┘         │      │
  │   │       │   │            GND    GND
  └───┴───────┴───┘
      │       │
     I2C Bus (shared)
```

### Battery Voltage Divider

Connect battery monitoring circuit:

```
Battery + ────[10kΩ]────┬────[10kΩ]──── GND
                        │
                        └─────────────► A0
```

This divider provides 50% of battery voltage to A0 for monitoring.

## Assembly Instructions

### Step 1: Prepare Components

1. Gather all components listed in BOM
2. Test each component individually before assembly:
   - Arduino Nano: Upload blink sketch
   - OLED Display: Run I2C scanner
   - RTC Module: Test with simple time sketch
3. Organize workspace with good lighting

### Step 2: Connect Display (OLED)

1. Connect OLED to Arduino:
   - VCC → 5V (or 3.3V depending on module)
   - GND → GND
   - SCL → A5
   - SDA → A4

2. Test display:
   ```cpp
   // Upload Adafruit SSD1306 example sketch
   // File → Examples → Adafruit SSD1306 → ssd1306_128x64_i2c
   ```

### Step 3: Connect RTC Module

1. Connect DS3231 to Arduino (shares I2C bus with OLED):
   - VCC → 5V
   - GND → GND
   - SCL → A5 (shared with OLED)
   - SDA → A4 (shared with OLED)

2. Insert CR2032 battery in RTC module for backup power

3. Test RTC:
   ```cpp
   // Upload RTClib example
   // File → Examples → RTClib → ds3231
   ```

### Step 4: Install Buttons

1. Connect three tactile buttons:
   
   **Button UP (D2)**:
   - One pin → D2
   - Other pin → GND
   
   **Button DOWN (D3)**:
   - One pin → D3
   - Other pin → GND
   
   **Button SELECT (D4)**:
   - One pin → D4
   - Other pin → GND

2. Internal pull-ups are enabled in code, no external resistors needed

### Step 5: Battery Circuit

1. Build voltage divider for battery monitoring:
   - Solder 10kΩ resistor from Battery+ to junction point
   - Solder 10kΩ resistor from junction point to GND
   - Connect junction point to A0

2. Connect TP4056 charging module:
   - Battery+ and Battery- to LiPo battery
   - OUT+ to Arduino VIN
   - OUT- to Arduino GND

3. **WARNING**: Never charge LiPo batteries unattended. Use proper charging modules with protection.

### Step 6: Optional Sensors

#### MPU6050 Accelerometer (for accurate step counting)

```
MPU6050          Arduino
VCC      →       3.3V
GND      →       GND
SCL      →       A5 (shared I2C)
SDA      →       A4 (shared I2C)
```

#### MAX30102 Heart Rate Sensor

```
MAX30102         Arduino
VIN      →       3.3V
GND      →       GND
SCL      →       A5 (shared I2C)
SDA      →       A4 (shared I2C)
```

### Step 7: Final Assembly

1. Organize components on breadboard or PCB
2. Double-check all connections
3. Ensure no short circuits
4. Test continuity with multimeter
5. Connect battery through charging module
6. Upload QP_WATCH_V13.ino sketch

## PCB Design (Optional)

For a permanent installation, consider designing a custom PCB:

### Recommended PCB Layout

- **Size**: 40mm x 40mm (or smaller for wrist mounting)
- **Layers**: 2-layer board
- **Components**: SMD or through-hole based on skill level
- **Mounting holes**: 4 corners for case attachment

### PCB Design Software

- **KiCad** (Free, Open Source)
- **EasyEDA** (Free, Web-based)
- **Eagle** (Free for hobbyists)

## 3D Printed Enclosure

### Case Design Specifications

- **Internal dimensions**: 45mm x 45mm x 15mm (minimum)
- **Display window**: 25mm x 15mm (for OLED)
- **Button access**: 3 side-mounted tactile switches
- **Battery compartment**: Dedicated space with secure retention
- **Charging port**: Access hole for USB connector

### Recommended Materials

- **PLA**: Easy to print, rigid
- **PETG**: More durable, slightly flexible
- **TPU**: Flexible, comfortable for wrist wear

### Watch Band Options

1. **22mm Standard Watch Strap**: Use standard watch band connectors
2. **3D Printed Band**: Design custom ergonomic band
3. **Velcro Strap**: Adjustable and comfortable

## Power Consumption Analysis

### Current Draw Estimates

| Component | Active Current | Sleep Current |
|-----------|----------------|---------------|
| Arduino Nano | 19mA | 5mA (sleep mode) |
| SSD1306 OLED | 20mA | 10μA (off) |
| DS3231 RTC | 200μA | 200μA |
| **Total Active** | **~40mA** | **~5mA** |

### Battery Life Calculations

With 500mAh battery:
- **Active use**: 500mAh / 40mA = 12.5 hours
- **With sleep mode** (30s timeout): ~24-36 hours
- **Deep sleep** (display off most of time): 2-3 days

With 1000mAh battery:
- **Active use**: 1000mAh / 40mA = 25 hours
- **With sleep mode**: ~48-72 hours
- **Deep sleep**: 4-6 days

## Troubleshooting Hardware Issues

### No Display

1. Check I2C address (use I2C scanner sketch)
2. Verify power supply voltage (3.3V or 5V)
3. Check SDA/SCL connections
4. Try different I2C pull-up resistor values (4.7kΩ)

### RTC Not Working

1. Ensure CR2032 battery is inserted correctly
2. Check I2C communication
3. Verify 32.768kHz crystal oscillator
4. Replace module if defective

### Buttons Not Responsive

1. Check button orientation (usually doesn't matter for tactile buttons)
2. Verify ground connections
3. Test with multimeter in continuity mode
4. Check for bent pins

### Poor Battery Life

1. Reduce display brightness
2. Decrease display update rate
3. Enable sleep mode more aggressively
4. Check for battery degradation
5. Ensure proper deep sleep implementation

### I2C Communication Errors

Multiple devices on I2C bus can cause issues:

1. Check all devices have unique addresses:
   - SSD1306: 0x3C or 0x3D
   - DS3231: 0x68
   - MPU6050: 0x68 or 0x69 (address conflict with RTC!)

2. If MPU6050 conflicts with DS3231:
   - Connect AD0 pin on MPU6050 to VCC to change address to 0x69

3. Add external pull-up resistors if multiple devices cause issues:
   - 4.7kΩ from SDA to VCC
   - 4.7kΩ from SCL to VCC

## Safety Guidelines

### LiPo Battery Safety

⚠️ **IMPORTANT WARNINGS**:

1. Never puncture or damage LiPo batteries
2. Use proper LiPo charger (TP4056 with protection)
3. Do not overcharge (>4.2V) or over-discharge (<3.0V)
4. Store at 3.7V-3.8V for long periods
5. Never charge unattended
6. Keep away from heat sources
7. Dispose of properly (recycling centers)

### General Electronics Safety

1. Double-check polarity before applying power
2. Use appropriate gauge wire for current levels
3. Ensure proper ventilation during operation
4. Avoid short circuits
5. Use ESD protection when handling components

## Maintenance

### Regular Maintenance

- **Weekly**: Check battery level, clean display
- **Monthly**: Verify RTC accuracy, check connections
- **Yearly**: Replace RTC backup battery if needed

### Component Lifespan

- **OLED Display**: 20,000-50,000 hours
- **LiPo Battery**: 300-500 charge cycles
- **RTC Battery**: 5-10 years
- **Arduino**: Indefinite (with proper care)

## Upgrades and Modifications

### Potential Upgrades

1. **Larger Battery**: Increase capacity for longer runtime
2. **Color Display**: ST7735 or ILI9341 TFT instead of OLED
3. **Wireless Charging**: Add Qi receiver module
4. **Bluetooth Module**: HC-05 or nRF24L01 for connectivity
5. **GPS Module**: NEO-6M for location tracking
6. **Solar Panel**: Small panel for trickle charging

### Advanced Modifications

1. Upgrade to ESP32 for WiFi/BLE capability
2. Add microSD card for data logging
3. Implement touchscreen with capacitive sensor
4. Add ambient light sensor for auto-brightness
5. Include haptic feedback motor for alerts

---

For additional support, consult:
- Arduino forums
- Adafruit learning guides
- Component datasheets
- QP Watch GitHub issues
