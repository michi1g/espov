#include "wifi_manager.h"
#include "web_server.h"
#include <ESP8266WiFi.h>

void WifiManager::begin(WebServerApp *web) {
  web_ = web;
  pinMode(CONFIG_BUTTON_PIN, INPUT_PULLUP);
  lastButton_ = digitalRead(CONFIG_BUTTON_PIN);

  WiFi.persistent(false);
  WiFi.mode(WIFI_OFF);
  mode_ = WifiMode::Off;
  applyCpuFreq();

  Serial.println(F("POV-Modus (WiFi aus). FLASH-Taste = Konfiguration."));
}

void WifiManager::applyCpuFreq() {
  if (mode_ == WifiMode::ConfigAp) {
    system_update_cpu_freq(CPU_FREQ_WIFI_MHZ);
  } else {
    system_update_cpu_freq(CPU_FREQ_POV_MHZ);
  }
}

bool WifiManager::buttonPressed() const {
  return digitalRead(CONFIG_BUTTON_PIN) == LOW;
}

void WifiManager::startConfigAp() {
  if (mode_ == WifiMode::ConfigAp) {
    notifyActivity();
    return;
  }

  WiFi.mode(WIFI_AP);
  WiFi.softAP(WIFI_AP_SSID, WIFI_AP_PASS);
  web_->startServer();
  mode_ = WifiMode::ConfigAp;
  apOffAt_ = millis() + WIFI_AP_TIMEOUT_MS;
  applyCpuFreq();

  Serial.print(F("Konfig-AP aktiv: "));
  Serial.println(WIFI_AP_SSID);
  Serial.print(F("IP: "));
  Serial.println(WiFi.softAPIP());
}

void WifiManager::stopConfigAp() {
  if (mode_ == WifiMode::Off) {
    return;
  }

  web_->stopServer();
  WiFi.softAPdisconnect(true);
  WiFi.mode(WIFI_OFF);
  mode_ = WifiMode::Off;
  applyCpuFreq();

  Serial.println(F("WiFi aus – Batterie sparen."));
}

void WifiManager::notifyActivity() {
  if (mode_ == WifiMode::ConfigAp) {
    apOffAt_ = millis() + WIFI_AP_ACTIVITY_EXTEND_MS;
  }
}

uint32_t WifiManager::remainingMs() const {
  if (mode_ != WifiMode::ConfigAp) {
    return 0;
  }
  unsigned long now = millis();
  if (apOffAt_ <= now) {
    return 0;
  }
  return apOffAt_ - now;
}

void WifiManager::handleButton() {
  bool pressed = buttonPressed();
  unsigned long now = millis();

  if (pressed != lastButton_ && now - lastDebounce_ > 50) {
    lastDebounce_ = now;
    if (pressed) {
      if (mode_ == WifiMode::Off) {
        startConfigAp();
      } else {
        stopConfigAp();
      }
    }
    lastButton_ = pressed;
  }
}

void WifiManager::checkTimeout() {
  if (mode_ == WifiMode::ConfigAp && millis() >= apOffAt_) {
    stopConfigAp();
  }
}

void WifiManager::tick() {
  handleButton();
  checkTimeout();
}
