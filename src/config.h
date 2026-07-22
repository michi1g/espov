#pragma once

#include <Arduino.h>
#include "config.h"

// Wemos D1 Mini onboard FLASH button (GPIO0, active LOW)
static const uint8_t CONFIG_BUTTON_PIN = 0;

// WiFi AP auto-off after inactivity (milliseconds)
static const uint32_t WIFI_AP_TIMEOUT_MS = 180000; // 3 minutes
static const uint32_t WIFI_AP_ACTIVITY_EXTEND_MS = 60000; // +1 min per save/status

// CPU frequency (MHz) – lower when WiFi off saves power on 2×AA
static const uint8_t CPU_FREQ_POV_MHZ = 80;
static const uint8_t CPU_FREQ_WIFI_MHZ = 160;

// Power: feed Wemos 5V pin from boost (2×AA) or USB-C (see docs/HARDWARE.md)
// Do NOT connect 2×AA directly to 5V without boost.

// Default timing: microseconds between columns while displaying
static const uint16_t DEFAULT_COLUMN_US = 1200;
static const uint16_t MIN_COLUMN_US = 400;
static const uint16_t MAX_COLUMN_US = 5000;

// Pattern limits
static const uint16_t MAX_PATTERN_WIDTH = 256;
static const uint8_t PATTERN_HEIGHT = 8;

// WiFi access point
static const char *WIFI_AP_SSID = "MiniPOV-WiFi";
static const char *WIFI_AP_PASS = "minipov123";

// LittleFS paths
static const char *PATTERN_FILE = "/pattern.json";

// Wemos D1 Mini GPIO pins for 8 POV LEDs (D1, D2, D4, D5, D6, D7, D8, D0)
static const uint8_t LED_PINS[8] = {5, 4, 2, 14, 12, 13, 15, 16};

enum class WifiMode : uint8_t { Off, ConfigAp };
