# QP Watch V13 - API Reference

## Table of Contents

1. [Core Functions](#core-functions)
2. [Display Functions](#display-functions)
3. [Button Handling](#button-handling)
4. [State Management](#state-management)
5. [Sensor Functions](#sensor-functions)
6. [Utility Functions](#utility-functions)

---

## Core Functions

### `setup()`

Initializes all hardware components and prepares the watch for operation.

**Initialization order:**
1. Serial communication
2. GPIO pins
3. Display (SSD1306)
4. Splash screen
5. RTC module
6. Initial state

**Example:**
```cpp
void setup() {
  Serial.begin(115200);
  // ... initialization code
}
```

---

### `loop()`

Main execution loop that handles:
- Sleep timeout monitoring
- Button input processing
- Display updates based on current state
- Step counting
- Battery monitoring

**Flow:**
```cpp
void loop() {
  checkSleepTimeout();
  handleButtons();
  updateDisplay();
  updateSensors();
  delay(100);
}
```

---

## Display Functions

### `showSplashScreen()`

Displays the QP Watch V13 boot screen.

**Usage:**
```cpp
showSplashScreen();
delay(2000); // Show for 2 seconds
```

**Output:**
- Watch name
- Version number
- Edition text

---

### `displayWatchface()`

Renders the current watchface based on selected style.

**Supported styles:**
- `STYLE_DIGITAL`: Time with seconds and full date
- `STYLE_ANALOG`: Traditional clock face
- `STYLE_MINIMAL`: Large time display only

**Features:**
- Battery indicator in top-right corner
- Automatic time updates
- Style switching with DOWN button

**Example:**
```cpp
if (currentState == STATE_WATCHFACE) {
  displayWatchface();
}
```

---

### `displayDigitalWatchface(DateTime now)`

Renders digital time display.

**Parameters:**
- `now` (DateTime): Current time from RTC

**Display format:**
```
     HH:MM:SS
   
   DD/MM/YYYY
```

**Features:**
- Leading zeros for single digits
- Centered text alignment
- Battery indicator

---

### `displayAnalogWatchface(DateTime now)`

Renders analog clock face.

**Parameters:**
- `now` (DateTime): Current time from RTC

**Components:**
- Clock circle (radius: 28 pixels)
- 12 hour marks
- Hour hand (short)
- Minute hand (long)
- Center dot

**Math:**
```cpp
hourAngle = (hour % 12 + minute / 60.0) * 30 * PI / 180
minuteAngle = minute * 6 * PI / 180
```

---

### `displayMinimalWatchface(DateTime now)`

Renders minimal time display.

**Parameters:**
- `now` (DateTime): Current time from RTC

**Features:**
- Large font size (3x)
- No seconds
- Day of week display
- Clean aesthetic

**Days array:**
```cpp
{"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"}
```

---

### `displayMenu()`

Renders the main menu interface.

**Features:**
- Scrollable menu items
- Highlight selected item (inverted colors)
- Header with divider line

**Menu items:**
1. Watchface
2. Steps
3. Heart Rate
4. Battery
5. Settings
6. Sleep

**Navigation:**
- UP/DOWN: Scroll through items
- SELECT: Choose item

---

### `displaySteps()`

Shows step counter interface.

**Display elements:**
- Step count (large text)
- Goal progress bar
- Steps label

**Progress calculation:**
```cpp
int progress = map(stepCount, 0, goalSteps, 0, 100);
```

**Goal:** 10,000 steps (configurable)

---

### `displayHeartRate()`

Shows heart rate monitoring interface.

**Display elements:**
- Heart rate value (BPM)
- Heart icon
- BPM label

**Note:** Current implementation uses simulated data.

**Simulation:**
```cpp
heartRate = 72 + random(-5, 5); // 67-77 BPM range
```

---

### `displayBattery()`

Shows battery status interface.

**Display elements:**
- Large battery icon
- Battery percentage (overlaid)
- Visual fill indicator

**Battery icon:**
- Size: 60x30 pixels
- Terminal: 5x14 pixels
- Fill: Proportional to charge level

---

### `displaySettings()`

Shows settings menu interface.

**Configurable settings:**
- Brightness (0-255)
- Auto Sleep (ON/OFF)
- Step Tracking (ON/OFF)

**Future settings:**
- Time format (12h/24h)
- Date format
- Language
- Alarm settings

---

### `displaySleep()`

Clears display and enters sleep mode.

**Behavior:**
- Clears all pixels
- Turns off display
- Sets `displayOn = false`

---

## Button Handling

### `handleButtons()`

Processes button input with debouncing.

**Debounce logic:**
```cpp
static unsigned long lastButtonPress = 0;
if (currentTime - lastButtonPress < 200) return;
```

**Buttons checked:**
- BUTTON_UP (D2)
- BUTTON_DOWN (D3)
- BUTTON_SELECT (D4)

**Effects:**
- Updates `lastActivityTime`
- Calls appropriate handler function

---

### `handleUpButton()`

Processes UP button press.

**Actions by state:**
- `STATE_WATCHFACE`: Open menu
- `STATE_MENU`: Navigate up in menu
- `STATE_SLEEP`: Wake up watch

**Example:**
```cpp
if (currentState == STATE_WATCHFACE) {
  currentState = STATE_MENU;
  menuSelectedIndex = 0;
}
```

---

### `handleDownButton()`

Processes DOWN button press.

**Actions by state:**
- `STATE_WATCHFACE`: Cycle watchface styles
- `STATE_MENU`: Navigate down in menu

**Watchface cycling:**
```cpp
watchfaceStyle = (WatchfaceStyle)((watchfaceStyle + 1) % 3);
```

---

### `handleSelectButton()`

Processes SELECT button press.

**Actions by state:**
- `STATE_MENU`: Execute selected menu item
- Other states: Return to menu

**Menu selection logic:**
```cpp
switch (menuSelectedIndex) {
  case 0: currentState = STATE_WATCHFACE; break;
  case 1: currentState = STATE_STEPS; break;
  // ... more cases
}
```

---

## State Management

### States Enum

```cpp
enum WatchState {
  STATE_WATCHFACE,   // Main watch display
  STATE_MENU,        // Menu navigation
  STATE_STEPS,       // Step counter view
  STATE_HEART_RATE,  // Heart rate monitor
  STATE_SETTINGS,    // Settings configuration
  STATE_BATTERY,     // Battery status
  STATE_SLEEP        // Sleep/off mode
};
```

### State Transitions

```
WATCHFACE ←→ MENU ←→ STEPS
              ↕
          HEART_RATE
              ↕
           BATTERY
              ↕
          SETTINGS
              ↕
            SLEEP
```

---

### `enterSleepMode()`

Transitions to sleep state.

**Actions:**
- Sets `currentState = STATE_SLEEP`
- Sets `displayOn = false`
- Clears display

**Wake up:** Press any button

---

## Sensor Functions

### `updateStepCount()`

Updates step counter (simulated).

**Current implementation:**
- Adds random steps every 5 seconds
- Range: 0-10 steps per update

**For MPU6050 integration:**
```cpp
// Read accelerometer
int16_t ax, ay, az;
mpu.getAcceleration(&ax, &ay, &az);

// Detect step based on acceleration threshold
if (abs(ay) > STEP_THRESHOLD) {
  stepCount++;
}
```

---

### `updateBatteryLevel()`

Monitors battery voltage and updates level.

**Measurement:**
- Reads analog pin A0
- Updates every 10 seconds
- Maps ADC value to percentage

**Formula:**
```cpp
int rawValue = analogRead(BATTERY_PIN);
batteryLevel = map(rawValue, 0, 1023, 0, 100);
```

**Voltage divider required:**
- R1: 10kΩ (Battery+ to A0)
- R2: 10kΩ (A0 to GND)

---

## Utility Functions

### Time Functions

**Get current time:**
```cpp
DateTime now = rtc.now();
int hour = now.hour();
int minute = now.minute();
int second = now.second();
```

**Get current date:**
```cpp
int day = now.day();
int month = now.month();
int year = now.year();
int dayOfWeek = now.dayOfTheWeek(); // 0-6
```

**Set time:**
```cpp
rtc.adjust(DateTime(2026, 2, 11, 12, 30, 0));
// Format: (year, month, day, hour, minute, second)
```

---

### Display Helper Functions

**Clear display:**
```cpp
display.clearDisplay();
```

**Set text parameters:**
```cpp
display.setTextSize(2);     // 1-3
display.setTextColor(SSD1306_WHITE);
display.setCursor(x, y);
```

**Draw shapes:**
```cpp
display.drawCircle(x, y, radius, color);
display.fillCircle(x, y, radius, color);
display.drawRect(x, y, width, height, color);
display.fillRect(x, y, width, height, color);
display.drawLine(x1, y1, x2, y2, color);
```

**Update display:**
```cpp
display.display(); // Must call to show changes
```

---

### Math Helpers

**Map function:**
```cpp
int mapped = map(value, fromLow, fromHigh, toLow, toHigh);
```

**Example - Battery percentage:**
```cpp
int percent = map(voltage, 3.0, 4.2, 0, 100);
```

**Constrain function:**
```cpp
int constrained = constrain(value, min, max);
```

---

## Constants and Definitions

### Pin Definitions
```cpp
#define BUTTON_UP 2
#define BUTTON_DOWN 3
#define BUTTON_SELECT 4
#define BATTERY_PIN A0
#define LED_PIN 13
```

### Display Settings
```cpp
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define SCREEN_ADDRESS 0x3C
```

### Timing Constants
```cpp
const unsigned long SLEEP_TIMEOUT = 30000; // 30 seconds
```

---

## Global Variables

```cpp
WatchState currentState           // Current watch state
WatchfaceStyle watchfaceStyle     // Current watchface style
unsigned long stepCount           // Step counter
int heartRate                     // Heart rate (BPM)
int batteryLevel                  // Battery percentage
bool displayOn                    // Display power state
unsigned long lastActivityTime    // Last button press time
int menuSelectedIndex             // Selected menu item
int brightness                    // Display brightness
bool autoSleep                    // Auto-sleep enabled
bool stepTracking                 // Step tracking enabled
```

---

## Error Handling

### Display Initialization Error
```cpp
if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
  Serial.println(F("SSD1306 allocation failed"));
  while (1); // Halt
}
```

### RTC Initialization Error
```cpp
if (!rtc.begin()) {
  Serial.println(F("Couldn't find RTC"));
  // Show error on display
  while (1); // Halt
}
```

### RTC Power Loss
```cpp
if (rtc.lostPower()) {
  Serial.println(F("RTC lost power, setting time!"));
  rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
}
```

---

## Future API Extensions

### Planned Functions

**Notification handling:**
```cpp
void displayNotification(String message);
void vibrateAlert(int duration);
void playTone(int frequency, int duration);
```

**Alarm functions:**
```cpp
void setAlarm(int hour, int minute);
void checkAlarm();
void snoozeAlarm(int minutes);
```

**Data logging:**
```cpp
void logStepData();
void logHeartRateData();
void exportData();
```

**Connectivity:**
```cpp
void setupBluetooth();
void syncTime();
void receiveNotification();
```

---

## Best Practices

1. **Always check return values** for initialization functions
2. **Use F() macro** for string constants to save RAM
3. **Clear display** before drawing new content
4. **Call display.display()** to update screen
5. **Implement proper debouncing** for button inputs
6. **Monitor battery level** to prevent unexpected shutdowns
7. **Use millis()** instead of delay() for non-blocking code

---

For more examples and tutorials, see the `/examples` directory in the repository.
