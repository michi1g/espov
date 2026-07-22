#include <Arduino.h>
#include <LittleFS.h>
#include <WiFi.h>
#include "config.h"
#include "pattern_manager.h"
#include "pov_engine.h"
#include "web_server.h"
#include "wifi_manager.h"

PatternManager patterns;
PovEngine pov;
WebServerApp web;
WifiManager wifiMgr;

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println();
  Serial.println(F("MiniPOV WiFi – ESP8266 (2×AA-optimiert)"));

  pov.begin();

  if (!patterns.begin()) {
    Serial.println(F("LittleFS mount failed – formatting..."));
    LittleFS.format();
    patterns.begin();
  }

  pov.setPattern(patterns.data(), patterns.width());
  pov.setColumnDelayUs(patterns.columnDelayUs());

  web.begin(&patterns, &pov, &wifiMgr);
  wifiMgr.begin(&web);
}

void loop() {
  wifiMgr.tick();
  if (wifiMgr.isApActive()) {
    yield();
  }
  pov.tick();
}
