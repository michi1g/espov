#pragma once

#include <Arduino.h>
#include "config.h"

class PovEngine {
public:
  void begin();
  void setPattern(const uint8_t *data, uint16_t width);
  void setColumnDelayUs(uint16_t us);
  uint16_t columnDelayUs() const { return columnDelayUs_; }

  // Blocking POV display loop – call from main loop
  void tick();

  bool isDisplayEnabled() const { return displayEnabled_; }
  void setDisplayEnabled(bool enabled) { displayEnabled_ = enabled; }

private:
  void writeColumn(uint8_t columnByte);
  void allLedsOff();

  const uint8_t *patternData_ = nullptr;
  uint16_t patternWidth_ = 0;
  uint16_t columnIndex_ = 0;
  uint16_t columnDelayUs_ = DEFAULT_COLUMN_US;
  bool displayEnabled_ = true;
  unsigned long lastColumnUs_ = 0;

  // Precomputed GPOC/GPOS masks for fast GPIO on ESP8266
  uint32_t ledOnMasks_[8];
  uint32_t ledOffMasks_[8];
};
