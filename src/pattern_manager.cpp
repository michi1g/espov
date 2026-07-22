#include "pattern_manager.h"
#include <LittleFS.h>

bool PatternManager::begin() {
  if (!LittleFS.begin()) {
    return false;
  }
  return load();
}

bool PatternManager::load() {
  if (!LittleFS.exists(PATTERN_FILE)) {
    loadDemo();
    return save();
  }

  File f = LittleFS.open(PATTERN_FILE, "r");
  if (!f) {
    loadDemo();
    return false;
  }

  JsonDocument doc;
  DeserializationError err = deserializeJson(doc, f);
  f.close();

  if (err) {
    loadDemo();
    return false;
  }

  return setFromJson(doc);
}

bool PatternManager::save() {
  JsonDocument doc;
  toJson(doc);

  File f = LittleFS.open(PATTERN_FILE, "w");
  if (!f) {
    return false;
  }
  serializeJson(doc, f);
  f.close();
  return true;
}

bool PatternManager::setFromJson(JsonDocument &doc) {
  JsonArray arr = doc["data"].as<JsonArray>();
  if (arr.isNull() || arr.size() == 0 || arr.size() > MAX_PATTERN_WIDTH) {
    return false;
  }

  width_ = arr.size();
  for (uint16_t i = 0; i < width_; i++) {
    buffer_[i] = arr[i].as<uint8_t>();
  }

  columnDelayUs_ = doc["columnUs"] | DEFAULT_COLUMN_US;
  columnDelayUs_ = constrain(columnDelayUs_, MIN_COLUMN_US, MAX_COLUMN_US);
  return true;
}

void PatternManager::toJson(JsonDocument &doc) const {
  doc["width"] = width_;
  doc["columnUs"] = columnDelayUs_;
  JsonArray arr = doc["data"].to<JsonArray>();
  for (uint16_t i = 0; i < width_; i++) {
    arr.add(buffer_[i]);
  }
}

void PatternManager::loadDemo() {
  // Simple "HELLO" style demo – vertical bar sweep
  width_ = 32;
  for (uint16_t i = 0; i < width_; i++) {
    buffer_[i] = (1 << (i % 8));
  }
  columnDelayUs_ = DEFAULT_COLUMN_US;
}
