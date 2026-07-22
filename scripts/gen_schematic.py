#!/usr/bin/env python3
"""Generate a clean ESPOV KiCad 8 schematic with embedded symbols."""
from __future__ import annotations

import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "hardware" / "kicad" / "mini-pov-wifi.kicad_sch"


def uid() -> str:
    return str(uuid.uuid4())


def prop(name: str, value: str, x: float, y: float, hide: bool = False) -> str:
    hide_s = "\n          (hide yes)" if hide else ""
    return f"""      (property "{name}" "{value}"
        (at {x:.2f} {y:.2f} 0)
        (effects
          (font (size 1.27 1.27)){hide_s}
        )
      )"""


def symbol(lib_id: str, ref: str, value: str, x: float, y: float, pins: list[str],
           footprint: str = "", rot: int = 0) -> str:
    pin_block = "\n".join(f'    (pin "{p}" (uuid "{uid()}"))' for p in pins)
    return f'''  (symbol
    (lib_id "{lib_id}")
    (at {x:.2f} {y:.2f} {rot})
    (unit 1)
    (exclude_from_sim no)
    (in_bom yes)
    (on_board yes)
    (dnp no)
    (uuid "{uid()}")
{prop("Reference", ref, x + 2.54, y - 3.81)}
{prop("Value", value, x + 2.54, y - 1.27)}
{prop("Footprint", footprint, x, y, hide=True)}
{prop("Datasheet", "~", x, y, hide=True)}
{pin_block}
  )
'''


def wire(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'''  (wire (pts (xy {x1:.2f} {y1:.2f}) (xy {x2:.2f} {y2:.2f}))
    (stroke (width 0) (type default))
    (uuid "{uid()}")
  )
'''


def junction(x: float, y: float) -> str:
    return f'''  (junction (at {x:.2f} {y:.2f}) (diameter 0) (color 0 0 0 0)
    (uuid "{uid()}")
  )
'''


def label(name: str, x: float, y: float, justify: str = "left") -> str:
    return f'''  (label "{name}"
    (at {x:.2f} {y:.2f} 0)
    (effects (font (size 1.27 1.27)) (justify {justify}))
    (uuid "{uid()}")
  )
'''


def text(content: str, x: float, y: float, size: float = 1.5) -> str:
    return f'''  (text "{content}"
    (exclude_from_sim no)
    (at {x:.2f} {y:.2f} 0)
    (effects (font (size {size} {size}) (thickness 0.2)) (justify left top))
    (uuid "{uid()}")
  )
'''


def no_connect(x: float, y: float) -> str:
    return f'  (no_connect (at {x:.2f} {y:.2f}) (uuid "{uid()}"))\n'


LIB = r'''
  (lib_symbols
    (symbol "power:+5V"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "+5V" (at 0 3.556 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "+5V_0_1"
        (polyline (pts (xy -0.762 1.27) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 0) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 2.54) (xy 0.762 1.27)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "+5V_1_1"
        (pin power_in line (at 0 0 90) (length 0)
          (name "+5V" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "power:GND"
      (power) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "#PWR" (at 0 -6.35 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Value" "GND" (at 0 -3.81 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "GND_0_1"
        (polyline (pts (xy 0 0) (xy 0 -1.27) (xy 1.27 -1.27) (xy 0 -2.54) (xy -1.27 -1.27) (xy 0 -1.27))
          (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "GND_1_1"
        (pin power_in line (at 0 0 270) (length 0)
          (name "GND" (effects (font (size 1.27 1.27))))
          (number "1" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:R"
      (pin_numbers hide) (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "R" (at 2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Value" "R" (at -2.032 0 90) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "R_0_1"
        (rectangle (start -1.016 -2.54) (end 1.016 2.54)
          (stroke (width 0.254) (type default)) (fill (type none)))
      )
      (symbol "R_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:LED"
      (pin_numbers hide) (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "LED" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "LED_0_1"
        (polyline (pts (xy -1.27 -1.27) (xy -1.27 1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy -1.27 0) (xy 1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 1.27 -1.27) (xy 1.27 1.27) (xy -1.27 0) (xy 1.27 -1.27))
          (stroke (width 0.254) (type default)) (fill (type none)))
      )
      (symbol "LED_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54)
          (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 3.81 0 180) (length 2.54)
          (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:C"
      (pin_numbers hide) (pin_names (offset 0.254)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "C" (at 0.635 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "C" (at 0.635 -2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "C_0_1"
        (polyline (pts (xy -2.032 0.762) (xy 2.032 0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
        (polyline (pts (xy -2.032 -0.762) (xy 2.032 -0.762)) (stroke (width 0.508) (type default)) (fill (type none)))
      )
      (symbol "C_1_1"
        (pin passive line (at 0 3.81 270) (length 2.794)
          (name "~" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 2.794)
          (name "~" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:D_Schottky"
      (pin_numbers hide) (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "D" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Value" "D_Schottky" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "D_Schottky_0_1"
        (polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27)) (stroke (width 0.254) (type default)) (fill (type none)))
        (polyline (pts (xy 1.27 0) (xy -1.27 0)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 1.27 1.27) (xy 1.27 -1.27) (xy -1.27 0) (xy 1.27 1.27))
          (stroke (width 0.254) (type default)) (fill (type none)))
      )
      (symbol "D_Schottky_1_1"
        (pin passive line (at -3.81 0 0) (length 2.54)
          (name "K" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 3.81 0 180) (length 2.54)
          (name "A" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Device:Battery"
      (pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "BT" (at 2.54 2.54 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Value" "Battery" (at 2.54 0 0) (effects (font (size 1.27 1.27)) (justify left)))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "Battery_0_1"
        (rectangle (start -2.032 1.905) (end 2.032 1.27) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 1.905) (xy 0 2.54)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy 0 -2.54) (xy 0 -1.905)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy -1.016 0.635) (xy 1.016 0.635)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy -1.016 0) (xy 1.016 0)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy -1.016 -0.635) (xy 1.016 -0.635)) (stroke (width 0) (type default)) (fill (type none)))
        (polyline (pts (xy -1.524 -1.27) (xy 1.524 -1.27)) (stroke (width 0) (type default)) (fill (type none)))
      )
      (symbol "Battery_1_1"
        (pin passive line (at 0 3.81 270) (length 1.27)
          (name "+" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -3.81 90) (length 1.27)
          (name "-" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Connector:Conn_01x02"
      (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 3.81 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_01x02" (at 0 -5.08 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "Conn_01x02_1_1"
        (rectangle (start -1.27 -3.302) (end 0 2.032)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin passive line (at -5.08 1.27 0) (length 3.81)
          (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -5.08 -1.27 0) (length 3.81)
          (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "Connector:Conn_01x04"
      (pin_names (offset 1.016) (hide yes)) (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 6.35 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Conn_01x04" (at 0 -7.62 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "Conn_01x04_1_1"
        (rectangle (start -1.27 -6.35) (end 0 5.08)
          (stroke (width 0.254) (type default)) (fill (type background)))
        (pin passive line (at -5.08 3.81 0) (length 3.81)
          (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -5.08 1.27 0) (length 3.81)
          (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -5.08 -1.27 0) (length 3.81)
          (name "3" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin passive line (at -5.08 -3.81 0) (length 3.81)
          (name "4" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
      )
    )
    (symbol "espov:Wemos_D1_Mini"
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      (property "Reference" "U" (at 0 21.59 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Wemos_D1_Mini" (at 0 -21.59 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "mini-pov-wifi:Wemos_D1_Mini_Socket" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))
      (symbol "Wemos_D1_Mini_0_1"
        (rectangle (start -10.16 -20.32) (end 10.16 20.32)
          (stroke (width 0.254) (type default)) (fill (type background)))
      )
      (symbol "Wemos_D1_Mini_1_1"
        (pin power_in line (at -12.7 17.78 0) (length 2.54) (name "3V3" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at -12.7 15.24 0) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 12.7 0) (length 2.54) (name "D8" (effects (font (size 1.27 1.27)))) (number "3" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 10.16 0) (length 2.54) (name "D7" (effects (font (size 1.27 1.27)))) (number "4" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 7.62 0) (length 2.54) (name "D6" (effects (font (size 1.27 1.27)))) (number "5" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 5.08 0) (length 2.54) (name "D5" (effects (font (size 1.27 1.27)))) (number "6" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 2.54 0) (length 2.54) (name "D0" (effects (font (size 1.27 1.27)))) (number "7" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 0 0) (length 2.54) (name "CLK" (effects (font (size 1.27 1.27)))) (number "8" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 -2.54 0) (length 2.54) (name "MISO" (effects (font (size 1.27 1.27)))) (number "9" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at -12.7 -5.08 0) (length 2.54) (name "MOSI" (effects (font (size 1.27 1.27)))) (number "10" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 12.7 17.78 180) (length 2.54) (name "5V" (effects (font (size 1.27 1.27)))) (number "11" (effects (font (size 1.27 1.27)))))
        (pin power_in line (at 12.7 15.24 180) (length 2.54) (name "GND" (effects (font (size 1.27 1.27)))) (number "12" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 12.7 180) (length 2.54) (name "D4" (effects (font (size 1.27 1.27)))) (number "13" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 10.16 180) (length 2.54) (name "D3" (effects (font (size 1.27 1.27)))) (number "14" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 7.62 180) (length 2.54) (name "D2" (effects (font (size 1.27 1.27)))) (number "15" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 5.08 180) (length 2.54) (name "D1" (effects (font (size 1.27 1.27)))) (number "16" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 2.54 180) (length 2.54) (name "RX" (effects (font (size 1.27 1.27)))) (number "17" (effects (font (size 1.27 1.27)))))
        (pin bidirectional line (at 12.7 0 180) (length 2.54) (name "TX" (effects (font (size 1.27 1.27)))) (number "18" (effects (font (size 1.27 1.27)))))
        (pin input line (at 12.7 -2.54 180) (length 2.54) (name "RST" (effects (font (size 1.27 1.27)))) (number "19" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 12.7 -5.08 180) (length 2.54) (name "A0" (effects (font (size 1.27 1.27)))) (number "20" (effects (font (size 1.27 1.27)))))
      )
    )
  )
'''


def main() -> None:
    parts: list[str] = []
    wires: list[str] = []
    labels: list[str] = []
    junctions: list[str] = []
    texts: list[str] = []
    ncs: list[str] = []

    texts += [
        text("1. Power", 15.24, 12.7, 2.0),
        text("2. Controller", 120.65, 12.7, 2.0),
        text("3. POV LEDs", 210.82, 12.7, 2.0),
    ]

    # ----- Power -----
    # Battery
    parts.append(symbol("Device:Battery", "BT1", "2xAA", 30.48, 40.64, ["1", "2"],
                        "mini-pov-wifi:Battery_2xAA"))
    # BT1: + at (30.48, 36.83), - at (30.48, 44.45)

    # Boost connector: pin1 IN+, pin2 IN-, pin3 OUT+, pin4 OUT-
    parts.append(symbol("Connector:Conn_01x04", "U1", "MT3608", 60.96, 40.64, ["1", "2", "3", "4"],
                        "mini-pov-wifi:MT3608_Module"))
    # pins at x=55.88; y=44.45, 41.91, 39.37, 36.83
    labels += [
        label("IN+", 53.34, 44.45, "right"),
        label("IN-", 53.34, 41.91, "right"),
        label("OUT+", 53.34, 39.37, "right"),
        label("OUT-", 53.34, 36.83, "right"),
    ]

    # USB-C
    parts.append(symbol("Connector:Conn_01x02", "J2", "USB-C", 30.48, 71.12, ["1", "2"],
                        "mini-pov-wifi:USB-C_Breakout"))
    # pin1 VBUS (25.4, 72.39), pin2 GND (25.4, 69.85)
    labels += [
        label("VBUS", 22.86, 72.39, "right"),
        label("GND", 22.86, 69.85, "right"),
    ]

    # Schottky diodes rot=180 => A left, K right
    parts.append(symbol("Device:D_Schottky", "D9", "1N5817", 81.28, 39.37, ["1", "2"],
                        "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal", rot=180))
    parts.append(symbol("Device:D_Schottky", "D10", "1N5817", 81.28, 72.39, ["1", "2"],
                        "Diode_THT:D_DO-41_SOD81_P10.16mm_Horizontal", rot=180))
    # A at x-3.81=77.47, K at x+3.81=85.09

    # Caps
    parts.append(symbol("Device:C", "C1", "100uF", 106.68, 46.99, ["1", "2"],
                        "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm"))
    parts.append(symbol("Device:C", "C2", "100nF", 116.84, 46.99, ["1", "2"]))
    # pin1 top (x, y-3.81), pin2 bottom (x, y+3.81)

    # Power flags
    parts.append(symbol("power:+5V", "#PWR01", "+5V", 96.52, 27.94, ["1"]))
    parts.append(symbol("power:GND", "#PWR02", "GND", 96.52, 62.23, ["1"]))
    parts.append(symbol("power:+5V", "#PWR03", "+5V", 152.4, 27.94, ["1"]))
    parts.append(symbol("power:GND", "#PWR04", "GND", 152.4, 62.23, ["1"]))

    # Battery -> Boost
    wires += [
        wire(30.48, 36.83, 30.48, 25.4),
        wire(30.48, 25.4, 55.88, 25.4),
        wire(55.88, 25.4, 55.88, 44.45),  # IN+
        wire(30.48, 44.45, 30.48, 52.07),
        wire(30.48, 52.07, 55.88, 52.07),
        wire(55.88, 52.07, 55.88, 41.91),  # IN-
        wire(55.88, 52.07, 96.52, 52.07),  # GND rail
        wire(96.52, 52.07, 96.52, 62.23),
        wire(55.88, 36.83, 55.88, 52.07),  # OUT- to GND
    ]
    junctions += [junction(55.88, 52.07), junction(96.52, 52.07), junction(30.48, 52.07)]

    # Boost OUT+ -> D9 -> +5V
    wires += [
        wire(55.88, 39.37, 77.47, 39.37),
        wire(85.09, 39.37, 96.52, 39.37),
        wire(96.52, 39.37, 96.52, 27.94),
    ]
    junctions.append(junction(96.52, 39.37))

    # Caps on +5V
    wires += [
        wire(96.52, 39.37, 106.68, 39.37),
        wire(106.68, 39.37, 106.68, 43.18),
        wire(106.68, 50.8, 106.68, 52.07),
        wire(106.68, 52.07, 96.52, 52.07),
        wire(106.68, 39.37, 116.84, 39.37),
        wire(116.84, 39.37, 116.84, 43.18),
        wire(116.84, 50.8, 116.84, 52.07),
        wire(116.84, 52.07, 106.68, 52.07),
    ]
    junctions += [junction(106.68, 39.37), junction(106.68, 52.07),
                  junction(116.84, 39.37), junction(116.84, 52.07)]

    # USB-C -> D10 -> +5V, GND
    wires += [
        wire(25.4, 72.39, 77.47, 72.39),
        wire(85.09, 72.39, 96.52, 72.39),
        wire(96.52, 72.39, 96.52, 39.37),
        wire(25.4, 69.85, 25.4, 52.07),
        wire(25.4, 52.07, 30.48, 52.07),
    ]
    junctions += [junction(96.52, 72.39), junction(25.4, 52.07)]

    # Extend rails to MCU
    wires += [
        wire(96.52, 39.37, 152.4, 39.37),
        wire(152.4, 39.37, 152.4, 27.94),
        wire(96.52, 52.07, 152.4, 52.07),
        wire(152.4, 52.07, 152.4, 62.23),
    ]
    junctions += [junction(152.4, 39.37), junction(152.4, 52.07)]

    # ----- Wemos -----
    ux, uy = 165.1, 114.3
    parts.append(symbol("espov:Wemos_D1_Mini", "U2", "Wemos D1 Mini", ux, uy,
                        [str(i) for i in range(1, 21)],
                        "mini-pov-wifi:Wemos_D1_Mini_Socket"))
    left_x = ux - 12.7   # 152.4
    right_x = ux + 12.7  # 177.8

    # pin Y offsets from center
    left_pins = {
        "3V3": 17.78, "GNDL": 15.24, "D8": 12.7, "D7": 10.16, "D6": 7.62,
        "D5": 5.08, "D0": 2.54, "CLK": 0, "MISO": -2.54, "MOSI": -5.08,
    }
    right_pins = {
        "5V": 17.78, "GNDR": 15.24, "D4": 12.7, "D3": 10.16, "D2": 7.62,
        "D1": 5.08, "RX": 2.54, "TX": 0, "RST": -2.54, "A0": -5.08,
    }

    # 5V / GND to Wemos
    wires += [
        wire(152.4, 39.37, 177.8, 39.37),
        wire(177.8, 39.37, 177.8, uy + right_pins["5V"]),
        wire(152.4, 52.07, 152.4, uy + left_pins["GNDL"]),
        wire(152.4, uy + left_pins["GNDL"], left_x, uy + left_pins["GNDL"]),
        wire(177.8, uy + right_pins["GNDR"], 185.42, uy + right_pins["GNDR"]),
        wire(185.42, uy + right_pins["GNDR"], 185.42, 52.07),
        wire(185.42, 52.07, 152.4, 52.07),
    ]
    junctions += [
        junction(177.8, 39.37),
        junction(152.4, uy + left_pins["GNDL"]),
        junction(185.42, 52.07),
        junction(152.4, 52.07),
    ]

    # No-connects
    for name in ["3V3", "CLK", "MISO", "MOSI"]:
        ncs.append(no_connect(left_x, uy + left_pins[name]))
    for name in ["D3", "RX", "TX", "RST", "A0"]:
        ncs.append(no_connect(right_x, uy + right_pins[name]))

    # ----- LED array -----
    # GPIO map: LED index 1..8 -> pin
    gpio_map = [
        ("D1", right_x, uy + right_pins["D1"]),
        ("D2", right_x, uy + right_pins["D2"]),
        ("D4", right_x, uy + right_pins["D4"]),
        ("D5", left_x, uy + left_pins["D5"]),
        ("D6", left_x, uy + left_pins["D6"]),
        ("D7", left_x, uy + left_pins["D7"]),
        ("D8", left_x, uy + left_pins["D8"]),
        ("D0", left_x, uy + left_pins["D0"]),
    ]

    rx0 = 220.98  # resistor centers
    dx0 = 246.38  # LED centers
    gnd_bus = 259.08
    parts.append(symbol("power:GND", "#PWR05", "GND", gnd_bus, 152.4, ["1"]))

    bus_left = 200.66
    bus_right = 195.58

    for i, (gpio, gx, gy) in enumerate(gpio_map):
        y = 25.4 + i * 12.7
        idx = i + 1
        parts.append(symbol("Device:R", f"R{idx}", "100R", rx0, y, ["1", "2"],
                            "mini-pov-wifi:R_THT_1-4W", rot=90))
        parts.append(symbol("Device:LED", f"D{idx}", "LED", dx0, y, ["1", "2"],
                            "mini-pov-wifi:LED_D5.0mm", rot=180))

        r_l, r_r = rx0 - 3.81, rx0 + 3.81
        a, k = dx0 - 3.81, dx0 + 3.81

        if gx < ux:  # left side of MCU
            wires += [
                wire(gx, gy, bus_left, gy),
                wire(bus_left, gy, bus_left, y),
                wire(bus_left, y, r_l, y),
            ]
            junctions.append(junction(bus_left, y))
        else:
            wires += [
                wire(gx, gy, bus_right, gy),
                wire(bus_right, gy, bus_right, y),
                wire(bus_right, y, r_l, y),
            ]
            junctions.append(junction(bus_right, y))

        wires += [
            wire(r_r, y, a, y),
            wire(k, y, gnd_bus, y),
        ]
        labels.append(label(gpio, r_l - 1.27, y - 1.27, "right"))
        junctions.append(junction(gnd_bus, y))

    wires.append(wire(gnd_bus, 25.4, gnd_bus, 152.4))

    texts += [
        text("D9/D10 = Schottky OR (Boost + USB -> +5V)", 15.24, 90.17, 1.27),
        text("D3/FLASH = WiFi config button (on module)", 120.65, 152.4, 1.27),
        text("GPIO -> 100R -> LED Anode; Kathode -> GND", 210.82, 139.7, 1.27),
    ]

    body = "\n".join(texts + junctions + wires + labels + ncs + parts)
    sch = f'''(kicad_sch
  (version 20231120)
  (generator "eeschema")
  (generator_version "8.0")
  (uuid "{uid()}")
  (paper "A3")
  (title_block
    (title "ESPOV - MiniPOV WiFi")
    (date "2026-07-22")
    (rev "0.3")
    (company "")
    (comment 1 "ESP8266 POV - 2xAA + Boost + USB-C")
    (comment 2 "Embedded symbols - footprints in mini-pov-wifi.pretty")
    (comment 3 "docs/HARDWARE.md")
  )
{LIB}
{body}
  (sheet_instances
    (path "/" (page "1"))
  )
)
'''
    OUT.write_text(sch, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT}")
    print(f"symbols={len(parts)} wires={len(wires)} labels={len(labels)}")


if __name__ == "__main__":
    main()
