#include "pov_engine.h"

// ESP8266 GPIO register helpers
#define GPOS (*((volatile uint32_t *)0x60000304))
#define GPOC (*((volatile uint32_t *)0x60000308))

void PovEngine::begin() {
  for (uint8_t i = 0; i < 8; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    digitalWrite(LED_PINS[i], LOW);
    ledOnMasks_[i] = (1UL << LED_PINS[i]);
    ledOffMasks_[i] = (1UL << LED_PINS[i]);
  }
}

void PovEngine::setPattern(const uint8_t *data, uint16_t width) {
  patternData_ = data;
  patternWidth_ = width;
  columnIndex_ = 0;
}

void PovEngine::setColumnDelayUs(uint16_t us) {
  columnDelayUs_ = constrain(us, MIN_COLUMN_US, MAX_COLUMN_US);
}

void PovEngine::allLedsOff() {
  for (uint8_t i = 0; i < 8; i++) {
    GPOC = ledOffMasks_[i];
  }
}

void PovEngine::writeColumn(uint8_t columnByte) {
  for (uint8_t i = 0; i < 8; i++) {
    if (columnByte & (1 << i)) {
      GPOS = ledOnMasks_[i];
    } else {
      GPOC = ledOffMasks_[i];
    }
  }
}

void PovEngine::tick() {
  if (!displayEnabled_ || !patternData_ || patternWidth_ == 0) {
    return;
  }

  unsigned long now = micros();
  if (now - lastColumnUs_ < columnDelayUs_) {
    return;
  }
  lastColumnUs_ = now;

  writeColumn(patternData_[columnIndex_]);
  columnIndex_++;
  if (columnIndex_ >= patternWidth_) {
    columnIndex_ = 0;
    allLedsOff();
    delayMicroseconds(columnDelayUs_ * 4); // brief gap between repeats
  }
}
