# Contributing to QP Watch

First off, thank you for considering contributing to QP Watch! It's people like you that make QP Watch such a great tool.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How Can I Contribute?](#how-can-i-contribute)
4. [Development Guidelines](#development-guidelines)
5. [Coding Standards](#coding-standards)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all.

### Our Standards

- Be respectful and inclusive
- Welcome newcomers warmly
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/QP_WATCH_V001.git
   cd QP_WATCH_V001
   ```

3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up your development environment**:
   - Install Arduino IDE (1.8.x or 2.x)
   - Install required libraries (see README.md)
   - Connect your hardware for testing

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

**When submitting a bug report, include:**
- Clear and descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Hardware configuration (Arduino model, display type, etc.)
- Software versions (Arduino IDE, libraries)
- Serial monitor output (if applicable)
- Photos or screenshots (if relevant)

**Example bug report:**
```markdown
**Bug**: Display shows garbled text on startup

**Hardware**:
- Arduino Nano clone
- SSD1306 0.96" OLED (I2C)
- DS3231 RTC module

**Steps to Reproduce**:
1. Upload QP_WATCH_V13.ino
2. Power on the device
3. Display shows random characters

**Expected**: Should show splash screen with "QP WATCH" text

**Serial Output**:
```
QP Watch V13 - Starting...
SSD1306 allocation failed
```
```

### Suggesting Features

Feature suggestions are welcome! Please:

1. **Check existing issues** for similar suggestions
2. **Use a clear title** describing the feature
3. **Provide detailed description** of the feature
4. **Explain why this feature would be useful**
5. **Include examples** or mockups if applicable

**Example feature request:**
```markdown
**Feature**: Add stopwatch mode

**Description**: 
Add a stopwatch function accessible from the menu that allows users to 
time activities with lap recording.

**Use Case**:
Useful for timing workouts, cooking, or any timed activities.

**Implementation Ideas**:
- New menu item "Stopwatch"
- Display showing MM:SS.MS format
- Lap time recording (up to 10 laps)
- Controls: SELECT=Start/Stop, UP=Lap, DOWN=Reset
```

### Code Contributions

We love pull requests! Here's what we're looking for:

**Good contributions:**
- Bug fixes
- New features (discussed in issues first)
- Documentation improvements
- Performance optimizations
- Better error handling
- Additional watchface styles
- Sensor integrations

**Please avoid:**
- Large refactoring without discussion
- Breaking backward compatibility
- Adding dependencies unnecessarily
- Changing code style throughout the file

## Development Guidelines

### Setting Up Development Environment

1. **Hardware Setup**:
   - Assemble the watch according to HARDWARE_GUIDE.md
   - Keep serial connection available for debugging
   - Use a breadboard for initial development

2. **Software Setup**:
   ```bash
   # Install Arduino CLI (optional but recommended)
   curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
   
   # Install required libraries
   arduino-cli lib install "Adafruit GFX Library"
   arduino-cli lib install "Adafruit SSD1306"
   arduino-cli lib install "RTClib"
   ```

3. **Testing Setup**:
   - Use Serial Monitor at 115200 baud
   - Enable DEBUG_MODE in configuration
   - Keep notes of your tests

### Development Workflow

1. **Create an issue** (or comment on existing one)
2. **Fork and clone** the repository
3. **Create a feature branch**:
   ```bash
   git checkout -b feature/add-stopwatch
   ```

4. **Make your changes**:
   - Write clean, commented code
   - Follow existing code style
   - Test thoroughly on hardware

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add stopwatch feature with lap timing"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/add-stopwatch
   ```

7. **Open a Pull Request**

## Coding Standards

### General Principles

- **Keep it simple**: Avoid overcomplicating solutions
- **Comment your code**: Explain why, not just what
- **Be consistent**: Follow existing patterns
- **Optimize carefully**: Readability first, then optimize

### Arduino C++ Style Guide

#### Naming Conventions

```cpp
// Constants: UPPER_CASE with underscores
#define BUTTON_PIN 2
const int MAX_STEPS = 10000;

// Variables: camelCase
int stepCount = 0;
unsigned long lastUpdateTime = 0;

// Functions: camelCase
void updateDisplay() { }
void handleButtonPress() { }

// Classes/Enums: PascalCase
enum WatchState { ... };
class SensorManager { ... };
```

#### Code Structure

```cpp
// Function with proper comments
/**
 * Updates the step counter based on accelerometer data
 * 
 * @param threshold Detection threshold (higher = less sensitive)
 * @return true if step detected, false otherwise
 */
bool updateStepCounter(float threshold) {
  // Read accelerometer values
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  
  // Calculate magnitude
  float magnitude = sqrt(ax*ax + ay*ay + az*az);
  
  // Check against threshold
  if (magnitude > threshold) {
    stepCount++;
    return true;
  }
  
  return false;
}
```

#### Memory Optimization

```cpp
// Use F() macro for string constants to save RAM
Serial.println(F("QP Watch starting..."));
display.print(F("Steps: "));

// Use appropriate data types
uint8_t brightness = 128;  // 0-255 fits in byte
uint16_t stepCount = 0;    // Max 65,535 steps
uint32_t timestamp = 0;    // For millis() values

// Avoid String class, use char arrays
char buffer[16];
sprintf(buffer, "%02d:%02d", hour, minute);
```

#### Pin Definitions

```cpp
// Use descriptive names and comments
#define BUTTON_UP 2      // UP navigation button
#define BUTTON_DOWN 3    // DOWN navigation button  
#define BUTTON_SELECT 4  // SELECT/confirm button
#define BATTERY_PIN A0   // Battery voltage divider
```

### Documentation Standards

Every function should have:

```cpp
/**
 * Brief description of what the function does
 * 
 * Detailed explanation if needed, including:
 * - Algorithm explanation
 * - Important notes or warnings
 * - Side effects
 * 
 * @param paramName Description of parameter
 * @return Description of return value
 */
```

Example:
```cpp
/**
 * Displays the analog watchface with hour and minute hands
 * 
 * Draws a traditional clock face with:
 * - Circular border
 * - 12 hour marks
 * - Hour hand (short)
 * - Minute hand (long)
 * - Center pivot dot
 * 
 * Note: Second hand omitted to reduce visual clutter
 * 
 * @param now Current DateTime from RTC
 */
void displayAnalogWatchface(DateTime now) {
  // Implementation...
}
```

## Testing

### Hardware Testing Checklist

Before submitting, test on actual hardware:

- [ ] Code compiles without errors or warnings
- [ ] Display shows correctly (no corruption)
- [ ] All buttons respond properly
- [ ] Time keeps accurately
- [ ] Battery monitoring works
- [ ] Sleep mode activates and wakes correctly
- [ ] Memory usage is acceptable (<90% of RAM)
- [ ] No watchdog resets or crashes
- [ ] Serial debug output is clean

### Test on Multiple Configurations

If possible, test on:
- Different Arduino boards (Nano, Uno, etc.)
- Different display modules
- With and without optional sensors
- Different power supplies (USB, battery)

### Serial Monitor Testing

```cpp
// Add debug output for testing
#ifdef DEBUG_MODE
  Serial.print(F("Step count: "));
  Serial.println(stepCount);
  Serial.print(F("Free RAM: "));
  Serial.println(freeRam());
#endif
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if you changed functionality
2. **Add comments** to new code
3. **Test thoroughly** on hardware
4. **Check code compiles** without warnings
5. **Update CHANGELOG.md** with your changes

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Tested on hardware
- [ ] No compilation errors
- [ ] No new warnings
- [ ] All features still work
- [ ] Battery life not negatively impacted

## Hardware Tested On
- Arduino Nano v3
- SSD1306 0.96" OLED
- DS3231 RTC

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have commented my code
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have tested on actual hardware

## Screenshots (if UI changes)
[Add screenshots or photos]

## Additional Notes
[Any additional information]
```

### Review Process

1. **Automated checks** (if configured)
2. **Code review** by maintainers
3. **Testing** on reference hardware
4. **Feedback** and requested changes
5. **Approval** and merge

### After Your PR is Merged

- You can delete your branch
- Your contribution will be acknowledged in the changelog
- Thank you for contributing!

## Questions?

Feel free to ask questions by:
- Opening an issue with "Question:" prefix
- Commenting on existing issues
- Reaching out to maintainers

---

Thank you for contributing to QP Watch! Every contribution, no matter how small, helps make this project better.

**Happy Coding! 🎉**
