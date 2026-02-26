/*
 * QP Watch V13 - Configuration Example
 * 
 * This file shows various configuration options for customizing
 * your QP Watch. Copy the desired settings to your main sketch.
 */

// ============================================
// DISPLAY CONFIGURATION
// ============================================

// Choose your OLED display size
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// OLED I2C Address (usually 0x3C or 0x3D)
#define SCREEN_ADDRESS 0x3C

// Reset pin (use -1 if sharing Arduino reset pin)
#define OLED_RESET -1

// ============================================
// BUTTON CONFIGURATION
// ============================================

// Pin assignments for buttons
#define BUTTON_UP 2
#define BUTTON_DOWN 3
#define BUTTON_SELECT 4

// Button debounce delay (milliseconds)
#define BUTTON_DEBOUNCE 200

// ============================================
// POWER MANAGEMENT
// ============================================

// Auto-sleep timeout (milliseconds)
// Set to 0 to disable auto-sleep
const unsigned long SLEEP_TIMEOUT = 30000; // 30 seconds

// Enable/disable auto-sleep by default
bool autoSleep = true;

// Display brightness (0-255)
int brightness = 128;

// ============================================
// STEP COUNTER CONFIGURATION
// ============================================

// Enable step tracking
bool stepTracking = true;

// Daily step goal
#define STEP_GOAL 10000

// Step counter sensitivity (for accelerometer)
// Higher = less sensitive, Lower = more sensitive
#define STEP_THRESHOLD 1.5

// ============================================
// TIME AND DATE FORMAT
// ============================================

// Use 24-hour format (true) or 12-hour format (false)
#define TIME_24_HOUR true

// Date format options:
// 0 = DD/MM/YYYY
// 1 = MM/DD/YYYY
// 2 = YYYY-MM-DD
#define DATE_FORMAT 0

// ============================================
// WATCHFACE PREFERENCES
// ============================================

// Default watchface style
// 0 = STYLE_DIGITAL
// 1 = STYLE_ANALOG
// 2 = STYLE_MINIMAL
WatchfaceStyle watchfaceStyle = STYLE_DIGITAL;

// Show seconds on digital watchface
#define SHOW_SECONDS true

// Show battery indicator on watchface
#define SHOW_BATTERY true

// ============================================
// BATTERY MONITORING
// ============================================

// Battery voltage divider ratio
// For equal resistors (10k + 10k), use 2.0
#define BATTERY_DIVIDER 2.0

// Battery voltage range (in volts)
#define BATTERY_MIN_VOLTAGE 3.0
#define BATTERY_MAX_VOLTAGE 4.2

// Battery monitoring interval (milliseconds)
#define BATTERY_CHECK_INTERVAL 10000 // 10 seconds

// ============================================
// SENSOR CONFIGURATION
// ============================================

// Enable MPU6050 accelerometer
#define USE_MPU6050 false

// MPU6050 I2C address (0x68 or 0x69)
#define MPU6050_ADDRESS 0x69 // Use 0x69 to avoid conflict with RTC

// Enable MAX30102 heart rate sensor
#define USE_MAX30102 false

// MAX30102 I2C address
#define MAX30102_ADDRESS 0x57

// Heart rate update interval (milliseconds)
#define HR_UPDATE_INTERVAL 2000 // 2 seconds

// ============================================
// MENU CONFIGURATION
// ============================================

// Customize menu items (reorder or remove)
const char* menuItems[] = {
  "Watchface",
  "Steps",
  "Heart Rate",
  "Battery",
  "Settings",
  "Sleep"
};

// ============================================
// ADVANCED SETTINGS
// ============================================

// Serial debug output
#define DEBUG_MODE true

// Serial baud rate
#define SERIAL_BAUD 115200

// Display update interval (milliseconds)
#define DISPLAY_UPDATE_INTERVAL 100

// I2C clock speed (Hz)
// Standard: 100000, Fast: 400000
#define I2C_CLOCK 400000

// Enable watchdog timer for auto-reset on hang
#define USE_WATCHDOG false

// ============================================
// NOTIFICATIONS (Future Feature)
// ============================================

// Enable buzzer for notifications
#define USE_BUZZER false
#define BUZZER_PIN 9

// Enable vibration motor
#define USE_VIBRATION false
#define VIBRATION_PIN 10

// Notification duration (milliseconds)
#define NOTIFICATION_DURATION 1000

// ============================================
// CUSTOMIZATION EXAMPLES
// ============================================

/*
 * Example 1: Low Power Configuration
 * For maximum battery life
 * 
 * Note: To use these settings, modify the #define values in your main code
 * or declare them as variables instead of constants
 */
void configureLowPower() {
  // Runtime modifiable settings
  autoSleep = true;
  brightness = 64; // Low brightness
  stepTracking = false; // Disable step tracking
  
  // These require changing #define values in main code:
  // #define SLEEP_TIMEOUT 10000 // 10 seconds
  // #define DISPLAY_UPDATE_INTERVAL 1000 // Update less frequently
}

/*
 * Example 2: Fitness Focus Configuration
 * For active users who want comprehensive tracking
 * 
 * Note: Hardware-related settings require changing #define values in main code
 */
void configureFitness() {
  // Runtime modifiable settings
  autoSleep = false;
  brightness = 255; // Maximum brightness for outdoor use
  stepTracking = true;
  
  // These require changing #define values in main code:
  // #define STEP_GOAL 15000 // Higher daily goal
  // #define USE_MPU6050 true // Enable accurate step counting
  // #define USE_MAX30102 true // Enable heart rate monitoring
}

/*
 * Example 3: Minimal/Clean Configuration
 * For users who prefer simplicity
 * 
 * Note: Some settings require modifying the main code
 */
void configureMinimal() {
  // Runtime modifiable settings
  watchfaceStyle = STYLE_MINIMAL;
  autoSleep = true;
  stepTracking = false;
  
  // These require changing values in main code:
  // #define SHOW_SECONDS false
  // Reduced menu items array in main code
}

/*
 * Example 4: Developer/Debug Configuration
 * For development and testing
 * 
 * Note: Debug settings require modifying #define values in main code
 */
void configureDeveloper() {
  // Runtime modifiable settings
  autoSleep = false; // Stay awake for testing
  
  // These require changing #define values in main code:
  // #define DEBUG_MODE true
  // #define SERIAL_BAUD 115200
  // #define DISPLAY_UPDATE_INTERVAL 100 // Fast updates
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/*
 * Initialize all settings with defaults
 */
void initializeSettings() {
  // Apply default settings from this file
  Serial.println(F("Initializing settings..."));
  
  // Set I2C clock speed
  Wire.setClock(I2C_CLOCK);
  
  // Apply brightness (if supported by display)
  // Note: SSD1306 uses contrast, not brightness
  
  Serial.println(F("Settings initialized"));
}

/*
 * Save settings to EEPROM (for persistent storage)
 */
void saveSettings() {
  // TODO: Implement EEPROM storage
  // This would allow settings to persist across power cycles
}

/*
 * Load settings from EEPROM
 */
void loadSettings() {
  // TODO: Implement EEPROM loading
}

/*
 * Reset all settings to defaults
 */
void resetSettings() {
  autoSleep = true;
  brightness = 128;
  stepTracking = true;
  watchfaceStyle = STYLE_DIGITAL;
  Serial.println(F("Settings reset to defaults"));
}
