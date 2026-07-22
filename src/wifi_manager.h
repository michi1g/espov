#pragma once

#include <Arduino.h>
#include "config.h"

class WebServerApp;

class WifiManager {
public:
  void begin(WebServerApp *web);
  void tick();

  bool isApActive() const { return mode_ == WifiMode::ConfigAp; }
  uint32_t remainingMs() const;
  void notifyActivity();
  void startConfigAp();
  void stopConfigAp();

private:
  void applyCpuFreq();
  bool buttonPressed() const;
  void handleButton();
  void checkTimeout();

  WebServerApp *web_ = nullptr;
  WifiMode mode_ = WifiMode::Off;
  uint32_t apOffAt_ = 0;
  bool lastButton_ = true;
  unsigned long lastDebounce_ = 0;
};
