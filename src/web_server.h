#pragma once

#include <ESPAsyncWebServer.h>
#include "pattern_manager.h"
#include "pov_engine.h"

class WifiManager;

class WebServerApp {
public:
  void begin(PatternManager *patterns, PovEngine *pov, WifiManager *wifi);
  void startServer();
  void stopServer();
  bool isRunning() const { return running_; }

private:
  void setupRoutes();

  AsyncWebServer server_{80};
  PatternManager *patterns_ = nullptr;
  PovEngine *pov_ = nullptr;
  WifiManager *wifi_ = nullptr;
  bool running_ = false;
};
