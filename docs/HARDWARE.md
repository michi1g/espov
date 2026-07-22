# MiniPOV WiFi – Hardware

ESP8266-POV im Stil des [Adafruit MiniPOV3](https://learn.adafruit.com/minipov3), mit **2×AA-Betrieb**, optionalem **USB-C** und WiFi nur bei Bedarf.

## Stromversorgung – Übersicht

```
  2×AA (2,0–3,2 V)
       │
       ▼
  ┌─────────────┐
  │ Boost 5 V   │───|>───┐
  │ (MT3608 o.ä.)│       │
  └─────────────┘       ├──► 5 V Rail ──► Wemos D1 Mini (5V-Pin)
                        │
  USB-C Breakout 5 V ──|>──┘
       │
      GND ═══════════════════════ GND (gemeinsame Masse)
```

**Wichtig:** 2×AA **niemals** direkt an 5 V oder 3,3 V – der ESP8266 braucht einen **Boost-Wandler** (2×AA → 5 V).

Der Wemos D1 Mini hat einen onboard AMS1117 (5 V → 3,3 V). Beide Quellen speisen den **5V-Pin** über Schottky-Dioden (Verpolungsschutz + Quellenumschaltung).

| Quelle | Spannung | Anschluss | Verwendung |
|--------|----------|-----------|------------|
| 2× AA | 2,0–3,2 V | → Boost → 5 V Rail | POV unterwegs |
| USB-C | 5 V | Breakout → 5 V Rail | Laden/Programmieren am PC |
| Wemos Micro-USB | 5 V | onboard | Entwicklung (parallel möglich) |

### Erwartete Laufzeit (2×AA, alkalisch)

| Modus | Strom ca. | Laufzeit ca. |
|-------|-----------|--------------|
| POV, WiFi **aus** | 50–80 mA | **3–6 h** |
| Konfiguration, WiFi **an** | 120–180 mA | **1–2 h** gesamt* |

\*WiFi ist standardmäßig aus und nur 3 Minuten aktiv (FLASH-Taste). So bleibt die Batterie lange im POV-Modus.

## Stückliste (BOM)

| Menge | Bauteil | Beschreibung | Bezugsquelle / Hinweis |
|------:|---------|--------------|------------------------|
| 1 | Wemos D1 Mini | ESP8266, 3,3 V-Regler | |
| 8 | 5 mm LED rot, diffus | wie MiniPOV3 | Kathode zur Plattenkante |
| 8 | 100 Ω, 1/4 W | LED-Strombegrenzung | |
| 1 | Batteriehalter **2× AA** | wie Original-MiniPOV | |
| 1 | Boost-Modul **5 V** | MT3608, Pololu U1V10F5 o.ä. | Ausgang auf **5,0 V** einstellen |
| 2 | Schottky-Diode | 1N5817, SS14 | Boost + USB-C zum 5V-Rail |
| 1 | USB-C-Breakout | 16-Pin, **nur 5 V + GND** | siehe USB-C-Abschnitt |
| 1 | 100 µF Elko | 6,3 V+ | nahe 5V-Rail (Puffer) |
| 1 | 100 nF Keramik | | nahe Wemos 3,3 V |
| 1 | Lochrasterplatine | ca. 50×70 mm | oder eigene PCB |
| 2 | Stiftleiste 8-polig | female | Wemos steckbar |
| — | Litzenkabel | | |

**Nicht nötig:** 3×AA, Zener-Dioden (MiniPOV3-Programmer), extra Programmer.

## Boost-Wandler einstellen

1. Boost ** ohne Last** an 2×AA oder Labornetzgerät (2,5 V) hängen.
2. Multimeter an Boost-Ausgang: Poti drehen bis **5,0 V** (max. 5,2 V).
3. Erst dann mit Wemos verbinden.

Empfehlung: MT3608-Modul mit USB-Ausgang **nicht** verwenden – feste 5-V-Module oder einstellbare Boosts mit Multimeter-Abgleich.

## USB-C – Anschluss & Platzierung

Es wird ein einfaches **USB-C-Breakout-Board** (nur Strom, ohne Daten) genutzt – gut lötbar, kein SMD-Löten am Stecker selbst.

### Anschluss

| USB-C Breakout | MiniPOV-Platine |
|----------------|-----------------|
| VBUS (5 V) | → Schottky-Anode → 5 V Rail |
| GND | → GND |

**Keine Datenleitung nötig** – Programmierung läuft weiter über den Micro-USB des Wemos oder UART.

### Platzierungs-Optionen

```
Option A – Griffende (empfohlen)          Option B – Unterseite
┌──────────────────────────┐              ┌──────────────────────────┐
│  LED LED LED LED LED ... │              │  LED LED LED LED LED ... │
│  [Wemos]    [Boost]      │              │  [Wemos]    [Boost]      │
│  ═══ Batterie 2×AA ═══   │              │  ═══ Batterie 2×AA ═══   │
│              [USB-C]─────┤              │  ──────[USB-C]────────── │  ← flach, Kabel von unten
└──────────────────────────┘              └──────────────────────────┘

Option C – Seitenkante                    Option D – neben Wemos
┌──────────────────────────┐              ┌──────────────────────────┐
│[USB-C]                   │              │ [USB-C] [Wemos] [Boost]  │
│  LED LED LED LED ...     │              │  LED LED LED LED ...     │
└──────────────────────────┘              └──────────────────────────┘
```

| Option | Vorteil | Nachteil |
|--------|---------|----------|
| **A – Griffende** | Kabel stört nicht beim Schwenken | etwas mehr Länge |
| **B – Unterseite** | kompakte Bauform | Kabel unter der Hand |
| **C – Seitenkante** | kurzer Steckerweg | evtl. Wackelkontakt |
| **D – neben Wemos** | kurze Leiterbahnen | weniger Platz für Boost |

**Tipp:** USB-C-Breakout mit **Lochbohrungen** (2,54 mm Raster) auf die Platine schrauben/löten – hält mechanisch besser als nur 2 Drähte.

### USB-C vs. Micro-USB am Wemos

| Anschluss | Wofür |
|-----------|-------|
| **USB-C auf Platine** | Alltagsladung, Powerbank, Netzteil – ergonomisch platziert |
| **Micro-USB am Wemos** | Firmware flashen während der Entwicklung |

Beide können parallel an die 5-V-Rail (jeweils mit Schottky). Beim gleichzeitigen Anschließen gewinnt die höhere Spannung; Schottkys verhindern Rückspeisung in Boost oder USB-C-Quelle.

## Schaltplan (Detail)

```
                    ┌─────────────────────────────────────┐
  Boost OUT ──|>────┤ 5V                                  │
                    │         ┌──────────────┐            │
  USB-C 5V ───|>────┤         │ Wemos D1 Mini│            │
                    │    5V──►│              │            │
  (Micro-USB) ──────┤         │ D1..D0 ──────┼──► 8× LED │
                    │    GND──┤              │            │
  2×AA ──► Boost IN │         └──────────────┘            │
  GND ══════════════╧═════════════════════════════════════┘

  LED: GPIO → 100Ω → Anode → Kathode → GND
```

## Pinbelegung (LEDs)

| LED | D-Pin | GPIO | Boot-Hinweis |
|----:|-------|------|--------------|
| 1 | D1 | GPIO5 | — |
| 2 | D2 | GPIO4 | — |
| 3 | D4 | GPIO2 | onboard LED |
| 4 | D5 | GPIO14 | — |
| 5 | D6 | GPIO12 | HIGH beim Boot (LED aus) |
| 6 | D7 | GPIO13 | — |
| 7 | D8 | GPIO15 | LOW beim Boot (LED aus) |
| 8 | D0 | GPIO16 | — |

**Konfig-Taste:** onboard **FLASH** (GPIO0) – WiFi ein/aus, siehe README.

## Löten – Reihenfolge

1. USB-C-Breakout und Batteriehalter an der gewählten Position fixieren.
2. Boost-Modul löten (Eingang ← 2×AA, Ausgang → Schottky → 5V-Rail).
3. Schottkys und 100 µF an der 5V-Rail.
4. 8× Widerstand + 8× LED (Kathode zur Außenkante).
5. Wemos auf Stiftleiste setzen, 5V + GND + LED-Drähte verbinden.
6. Boost-Spannung ** ohne Wemos** auf 5,0 V einstellen, dann Wemos stecken.
7. Test: USB-C → LEDs blinken, POV ok; Batterie → dasselbe.

## WiFi / Batterie sparen (Firmware)

| Zustand | Verhalten |
|---------|-----------|
| **POV-Modus** (Standard) | WiFi aus, 80 MHz CPU, Muster läuft |
| **Konfig-Modus** | FLASH-Taste → AP 3 Min., dann automatisch aus |
| **Web-Aktivität** | Timer +1 Minute pro Speichern/Abruf |
| **Web-UI** | „WiFi beenden“ schaltet sofort ab |

## KiCad-Platine

Fertiges Layout-Projekt (28×118 mm, USB-C an Griffseite): **[KICAD.md](KICAD.md)** in `hardware/kicad/`

## Mechanik

Vier Bohrlöcher (wie MiniPOV3) für Montage an Stab/Fahrrad. USB-C an der **Griffseite** platzieren, damit das Ladekabel beim Schwenken nicht über die LEDs hängt.

## Sicherheit

- Boost-Ausgang ** nie** über 5,2 V einstellen.
- Schottkys nicht vergessen (Boost ↔ USB-C).
- Kurzschluss an Batterie vermeiden – Boost zieht sonst hohen Strom.
- Beim Löten am Wemos Hitze kurz halten.
