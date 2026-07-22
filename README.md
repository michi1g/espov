# MiniPOV WiFi

ESP8266-Nachbau des [Adafruit MiniPOV3](https://learn.adafruit.com/minipov3) mit WiFi-Web-Editor, **2×AA-Betrieb** und optionalem **USB-C**.

## Features

- 8-LED-POV-Display (Persistence of Vision)
- **2× AA** wie beim Original (+ Boost-Wandler auf 5 V)
- **USB-C** optional auf der Platine (Laden ohne Micro-USB-Kabel am Wemos)
- WiFi **nur bei Bedarf** – FLASH-Taste, Auto-Timeout nach 3 Min.
- Web-Editor: Pixel, Text, Bild-Upload, Vorschau

## Bedienung

### POV anzeigen (Standard)

1. Einschalten (Batterie oder USB-C)
2. Gerät schwenken – gespeichertes Muster erscheint
3. WiFi ist **aus** → maximale Batterielaufzeit

### Muster ändern

1. **FLASH-Taste** am Wemos D1 Mini drücken → WiFi-AP startet
2. Mit **`MiniPOV-WiFi`** verbinden (Passwort: `minipov123`)
3. Browser: **http://192.168.4.1**
4. Muster gestalten → **An Gerät senden**
5. **WiFi beenden** (Web-UI oder FLASH-Taste) → zurück zum POV-Modus

Nach 3 Minuten ohne Aktivität schaltet WiFi automatisch ab.

## Hardware

Stückliste, Boost-Einstellung, USB-C-Platzierung: **[docs/HARDWARE.md](docs/HARDWARE.md)**

KiCad-Platinenlayout (28×118 mm, USB-C an Griffseite): **[docs/KICAD.md](docs/KICAD.md)** · Projekt in `hardware/kicad/`

Kurz:

- 2×AA → Boost 5 V → Wemos 5V-Pin
- USB-C 5 V parallel (mit Schottky-Diode)
- 8× LED + 100 Ω wie MiniPOV3

## Software flashen

[PlatformIO](https://platformio.org/) (VS Code Extension):

```bash
pio run -t upload      # Firmware
pio run -t uploadfs    # Web-Oberfläche
pio device monitor
```

Erstes Flashen bequem über **Micro-USB am Wemos** (USB-C auf Platine reicht danach für Strom).

## Konfiguration

`src/config.h`:

| Konstante | Standard | Bedeutung |
|-----------|----------|-----------|
| `WIFI_AP_TIMEOUT_MS` | 180000 | AP-Dauer (3 Min.) |
| `CPU_FREQ_POV_MHZ` | 80 | CPU im POV-Modus |
| `CONFIG_BUTTON_PIN` | 0 | FLASH-Taste |

## Projektstruktur

```
mini-pov-wifi/
├── data/           # Web-UI (LittleFS)
├── docs/           # Hardware-Doku
├── src/
│   ├── wifi_manager.*   # WiFi ein/aus, Timeout
│   ├── pov_engine.*     # LED-Timing
│   └── web_server.*     # REST + Editor
└── platformio.ini
```

## Lizenz

MIT – inspiriert vom Adafruit MiniPOV3.
