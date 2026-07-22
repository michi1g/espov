#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>
#include "config.h"

class PatternManager {
public:
  bool begin();
  bool load();
  bool save();

  const uint8_t *data() const { return buffer_; }
  uint16_t width() const { return width_; }
  uint16_t columnDelayUs() const { return columnDelayUs_; }

  bool setFromJson(JsonDocument &doc);
  void toJson(JsonDocument &doc) const;
  void setColumnDelayUs(uint16_t us) { columnDelayUs_ = us; }

  // Built-in demo pattern (blinking chase)
  void loadDemo();

private:
  uint8_t buffer_[MAX_PATTERN_WIDTH];
  uint16_t width_ = 0;
  uint16_t columnDelayUs_ = DEFAULT_COLUMN_US;
};
