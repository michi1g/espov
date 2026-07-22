#include "web_server.h"
#include "wifi_manager.h"
#include <LittleFS.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "config.h"

void WebServerApp::begin(PatternManager *patterns, PovEngine *pov, WifiManager *wifi) {
  patterns_ = patterns;
  pov_ = pov;
  wifi_ = wifi;
  setupRoutes();
}

void WebServerApp::startServer() {
  if (!running_) {
    server_.begin();
    running_ = true;
  }
}

void WebServerApp::stopServer() {
  if (running_) {
    server_.end();
    running_ = false;
  }
}

void WebServerApp::setupRoutes() {
  server_.serveStatic("/", LittleFS, "/").setDefaultFile("index.html");

  server_.on("/api/status", HTTP_GET, [this](AsyncWebServerRequest *request) {
    wifi_->notifyActivity();
    JsonDocument doc;
    doc["ssid"] = WIFI_AP_SSID;
    doc["wifiActive"] = wifi_->isApActive();
    doc["wifiRemainingMs"] = wifi_->remainingMs();
    doc["ip"] = wifi_->isApActive() ? WiFi.softAPIP().toString() : "";
    doc["width"] = patterns_->width();
    doc["columnUs"] = patterns_->columnDelayUs();
    doc["display"] = pov_->isDisplayEnabled();

    String out;
    serializeJson(doc, out);
    request->send(200, "application/json", out);
  });

  server_.on("/api/wifi/start", HTTP_POST, [this](AsyncWebServerRequest *request) {
    wifi_->startConfigAp();
    request->send(200, "application/json", "{\"ok\":true}");
  });

  server_.on("/api/wifi/stop", HTTP_POST, [this](AsyncWebServerRequest *request) {
    wifi_->stopConfigAp();
    request->send(200, "application/json", "{\"ok\":true}");
  });

  server_.on("/api/pattern", HTTP_GET, [this](AsyncWebServerRequest *request) {
    wifi_->notifyActivity();
    JsonDocument doc;
    patterns_->toJson(doc);
    String out;
    serializeJson(doc, out);
    request->send(200, "application/json", out);
  });

  server_.on(
      "/api/pattern", HTTP_POST,
      [this](AsyncWebServerRequest *request) {},
      nullptr,
      [this](AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total) {
        static String body;
        if (index == 0) {
          body = "";
          body.reserve(total);
        }
        for (size_t i = 0; i < len; i++) {
          body += (char)data[i];
        }
        if (index + len < total) {
          return;
        }

        wifi_->notifyActivity();

        JsonDocument doc;
        DeserializationError err = deserializeJson(doc, body);
        if (err || !patterns_->setFromJson(doc)) {
          request->send(400, "application/json", "{\"error\":\"invalid pattern\"}");
          return;
        }

        patterns_->save();
        pov_->setPattern(patterns_->data(), patterns_->width());
        pov_->setColumnDelayUs(patterns_->columnDelayUs());

        request->send(200, "application/json", "{\"ok\":true}");
      });

  server_.on("/api/display", HTTP_POST, [this](AsyncWebServerRequest *request) {
    wifi_->notifyActivity();
    if (request->hasParam("enabled", true)) {
      bool enabled = request->getParam("enabled", true)->value() == "1";
      pov_->setDisplayEnabled(enabled);
    }
    request->send(200, "application/json", "{\"ok\":true}");
  });

  server_.onNotFound([](AsyncWebServerRequest *request) {
    request->send(404, "text/plain", "Not found");
  });
}
