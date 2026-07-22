# KiCad – MiniPOV WiFi Platine

Platinen-Skizze im MiniPOV3-Formfaktor mit **USB-C an der Griffseite** und Platz für **2×AA + Boost**.

## Dateien

```
hardware/kicad/
├── mini-pov-wifi.kicad_pro    ← Projekt öffnen
├── mini-pov-wifi.kicad_sch    ← Blocksdiagramm / Verdrahtungshinweise
├── mini-pov-wifi.kicad_pcb    ← Layout-Skizze (v0.1)
├── mini-pov-wifi.kicad_sym    ← Lokale Symbole
├── mini-pov-wifi.pretty/      ← Footprints (THT, lötbar)
├── fp-lib-table
└── sym-lib-table
```

**KiCad 7 oder 8** empfohlen. Projektordner `hardware/kicad/` in KiCad öffnen.

## Platinenmaß

| Parameter | Wert |
|-----------|------|
| Größe | **28 × 118 mm** |
| Dicke | 1,6 mm |
| Form | schmaler Stab (MiniPOV-artig, Mitte verbreitert für Wemos) |
| Löcher | 4× 3,2 mm Montage (wie MiniPOV3) |

## Layout (Draufsicht)

```
  TIP ── LEDs schauen nach links (Kathode ←)

        ┌── LED-Reihe (D1–D8) ──────────────┐
        │  ● ● ● ● ● ● ● ●                  │  Y ≈ 8–61 mm
        │  R  R  R  R  R  R  R  R            │  Widerstände rechts
        │                                   │
        │      ┌─────────────┐              │
        │      │ Wemos D1    │              │  Y ≈ 68–96 mm
        │      │ Mini U2     │              │
        │      └─────────────┘              │
        │   [ MT3608 U1 ]  C1  D9 D10       │  Y ≈ 92 mm
        │      ( Boost )                    │
        │   [ 2×AA BT1 ]                    │  Y ≈ 102 mm
        │   ┌──────────┐                    │
  GRIFF │   │ USB-C J2 │                    │  Y ≈ 108 mm  ← hier laden
        └───┴──────────┴────────────────────┘
            H3                    H4
     H1                              H2  (Montagelöcher)
```

**Schwenkrichtung:** Griff unten halten, LEDs oben/links – wie beim Original-MiniPOV.

## Bauteil-Platzierung

| Ref | Bauteil | Position (ca.) | Hinweis |
|-----|---------|----------------|---------|
| D1–D8 | 5 mm LED | Spitze, 7,62 mm Pitch | 90° gedreht, Kathode zum linken Rand |
| R1–R8 | 100 Ω | rechts neben LEDs | GPIO → R → LED-Anode |
| U2 | Wemos D1 Mini | Mitte | 2×8 Stiftleisten, steckbar |
| U1 | MT3608-Modul | vor Griff | Ausgang auf **5,0 V** einstellen |
| BT1 | 2×AA-Anschluss | über Boost | +/- Litzen |
| J2 | USB-C-Breakout | **Griffseite** | nur VBUS + GND |
| D9, D10 | 1N5817 Schottky | nahe Boost | noch manuell platzieren / routen |
| C1 | 100 µF | nahe 5V-Rail | |
| C2 | 100 nF | nahe Wemos | |
| H1–H4 | 3,2 mm Bohrung | Ecken | Stab/Fahrrad-Montage |

## GPIO → LED (Firmware)

| LED | Wemos Pin | GPIO |
|----:|-----------|------|
| D1 | D1 | GPIO5 |
| D2 | D2 | GPIO4 |
| D3 | D4 | GPIO2 |
| D4 | D5 | GPIO14 |
| D5 | D6 | GPIO12 |
| D6 | D7 | GPIO13 |
| D7 | D8 | GPIO15 |
| D8 | D0 | GPIO16 |

## Nächste Schritte in KiCad

1. **Projekt öffnen** → PCB Editor
2. **D9, D10, C1, C2** Footprints aus `Device`-Library setzen und platzieren
3. **Netliste** aus Schematic aktualisieren (oder manuell routen wie Skizze)
4. **DRC** ausführen, Leiterbahnen vervollständigen
5. **3D-Ansicht** prüfen: USB-C-Stecker ragt am Griff heraus
6. **Gerber exportieren** (JLCPCB, PCBWay, …)

## Footprint anpassen

Falls dein USB-C-Breakout abweicht: Footprint `USB-C_Breakout` in `mini-pov-wifi.pretty/` editieren (Bohrabstand messen!).

MT3608-Module variieren leicht in der Größe – Pin-Abstand vor dem Löten prüfen.

## Bestellung

| Layer | Empfehlung |
|-------|------------|
| Kupfer | 1 Lage (F.Cu) reicht |
| Farbe | deine Wahl |
| Oberfläche | HASL oder ENIG |
| Stärke | 1,6 mm |

**THT-only** (außer optional SMD-Schottkys) – gut für Anfänger-Lötkurse.

## Export

```bash
# KiCad CLI (falls installiert)
kicad-cli pcb export gerbers hardware/kicad/mini-pov-wifi.kicad_pcb -o hardware/gerbers/
kicad-cli pcb export svg hardware/kicad/mini-pov-wifi.kicad_pcb -o hardware/exports/
```

## Status v0.1

Diese Version ist eine **Platzier-Skizze**:

- Board-Umriss und Bauteile platziert
- Strom-Rückgrat (+5V/GND) angedeutet
- Schottky-Dioden und Kondensatoren als Silkscreen-Hinweis
- Vollständiges Routing und ERC/DRC musst du in KiCad abschließen

Bei Fragen zur Verdrahtung: [HARDWARE.md](../HARDWARE.md)
