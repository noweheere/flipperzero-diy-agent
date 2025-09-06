#!/usr/bin/env python3
"""
Pinout Generator für Flipper Zero DIY-Erweiterungen

Dieses Modul generiert ASCII- und grafische Pinout-Darstellungen für verschiedene
Flipper Zero Anschlussarten: UART, FTDI, Direktanschluss und USB.
"""

import sys
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ConnectionType(Enum):
    """Verfügbare Anschlussarten für Flipper Zero"""
    UART = "uart"
    FTDI = "ftdi"
    DIRECT = "direct"
    USB = "usb"


class PinoutGenerator:
    """Hauptklasse für die Generierung von Pinout-Diagrammen"""
    
    def __init__(self):
        self.flipper_gpio_pins = {
            1: "VCC (3.3V)",
            2: "PA7 (SPI_MOSI)",
            3: "PA6 (SPI_MISO)", 
            4: "PA4 (SPI_SCK)",
            5: "PB3 (SPI_CS)",
            6: "PB2 (USART_TX)",
            7: "PC3 (USART_RX)",
            8: "PC1 (GPIO)",
            9: "PC0 (GPIO)",
            10: "PB8 (I2C_SCL)",
            11: "PB9 (I2C_SDA)",
            12: "PA15 (GPIO)",
            13: "PA14 (SWCLK)",
            14: "PA13 (SWDIO)",
            15: "RESET",
            16: "GND",
            17: "3V3 (Power Out)",
            18: "5V (USB Power)"
        }
        
        self.connection_configs = {
            ConnectionType.UART: {
                "pins": {6: "TX", 7: "RX", 1: "VCC", 16: "GND"},
                "description": "Standard UART Verbindung",
                "baudrate": "115200"
            },
            ConnectionType.FTDI: {
                "pins": {6: "TXD", 7: "RXD", 1: "VCC", 16: "GND"},
                "description": "FTDI USB-Serial Adapter",
                "voltage": "3.3V"
            },
            ConnectionType.DIRECT: {
                "pins": {8: "GPIO1", 9: "GPIO2", 12: "GPIO3", 1: "VCC", 16: "GND"},
                "description": "Direkte GPIO Verbindung",
                "note": "Für custom Hardware"
            },
            ConnectionType.USB: {
                "pins": {18: "5V", 16: "GND", "USB_D+": "Data+", "USB_D-": "Data-"},
                "description": "USB Verbindung",
                "protocol": "USB 2.0 Full Speed"
            }
        }
    
    def generate_ascii_pinout(self, connection_type: ConnectionType, width: int = 60) -> str:
        """Generiert ASCII-Pinout-Diagramm für den gewählten Verbindungstyp"""
        config = self.connection_configs.get(connection_type)
        if not config:
            raise ValueError(f"Unbekannter Verbindungstyp: {connection_type}")
        
        title = f"Flipper Zero {connection_type.value.upper()} Pinout"
        separator = "═" * width
        
        ascii_art = [
            f"╔{separator}╗",
            f"║{title:^{width}}║",
            f"║{config['description']:^{width}}║",
            f"╠{separator}╣"
        ]
        
        # Flipper Zero GPIO Header visualisieren
        ascii_art.extend([
            "║                    Flipper Zero GPIO                    ║",
            "║    ┌─────────────────────────────────────────────┐    ║",
            "║    │  1  3  5  7  9 11 13 15 17              │    ║",
            "║    │  o  o  o  o  o  o  o  o  o               │    ║",
            "║    │  o  o  o  o  o  o  o  o  o               │    ║",
            "║    │  2  4  6  8 10 12 14 16 18              │    ║",
            "║    └─────────────────────────────────────────────┘    ║",
            f"╠{separator}╣"
        ])
        
        # Pin-Zuordnungen
        ascii_art.append("║                    Pin-Zuordnungen                     ║")
        ascii_art.append(f"╠{separator}╣")
        
        for pin, function in config["pins"].items():
            if isinstance(pin, int):
                pin_desc = self.flipper_gpio_pins.get(pin, "Unknown")
                line = f"║ Pin {pin:2d}: {function:<10} → {pin_desc:<25} ║"
            else:
                line = f"║ {pin}: {function:<35} ║"
            ascii_art.append(line)
        
        # Zusätzliche Informationen
        ascii_art.append(f"╠{separator}╣")
        if "baudrate" in config:
            ascii_art.append(f"║ Baudrate: {config['baudrate']:<46} ║")
        if "voltage" in config:
            ascii_art.append(f"║ Spannung: {config['voltage']:<46} ║")
        if "protocol" in config:
            ascii_art.append(f"║ Protokoll: {config['protocol']:<45} ║")
        if "note" in config:
            ascii_art.append(f"║ Hinweis: {config['note']:<47} ║")
        
        ascii_art.append(f"╚{separator}╝")
        
        return "\n".join(ascii_art)
    
    def generate_connection_diagram(self, connection_type: ConnectionType) -> str:
        """Generiert ein detailliertes Verbindungsdiagramm"""
        config = self.connection_configs.get(connection_type)
        if not config:
            raise ValueError(f"Unbekannter Verbindungstyp: {connection_type}")
        
        diagram = []
        diagram.append(f"\n{connection_type.value.upper()} Verbindungsdiagramm:")
        diagram.append("=" * 50)
        
        if connection_type == ConnectionType.UART:
            diagram.extend([
                "Flipper Zero    ←→    UART Device",
                "Pin 6 (TX)      ←→    RX",
                "Pin 7 (RX)      ←→    TX", 
                "Pin 1 (VCC)     ←→    VCC (3.3V)",
                "Pin 16 (GND)    ←→    GND",
                "",
                "Baudrate: 115200, 8N1"
            ])
        
        elif connection_type == ConnectionType.FTDI:
            diagram.extend([
                "Flipper Zero    ←→    FTDI Adapter    ←→    USB",
                "Pin 6 (TX)      ←→    RXD",
                "Pin 7 (RX)      ←→    TXD",
                "Pin 1 (VCC)     ←→    VCC (3.3V)",
                "Pin 16 (GND)    ←→    GND",
                "",
                "⚠️  FTDI auf 3.3V einstellen!"
            ])
        
        elif connection_type == ConnectionType.DIRECT:
            diagram.extend([
                "Flipper Zero    ←→    Custom Hardware",
                "Pin 8 (PC1)     ←→    GPIO Input/Output",
                "Pin 9 (PC0)     ←→    GPIO Input/Output",
                "Pin 12 (PA15)   ←→    GPIO Input/Output",
                "Pin 1 (VCC)     ←→    Power (3.3V)",
                "Pin 16 (GND)    ←→    Ground",
                "",
                "⚠️  GPIO Level: 3.3V max!"
            ])
        
        elif connection_type == ConnectionType.USB:
            diagram.extend([
                "Flipper Zero USB-C    ←→    Host Device",
                "USB D+               ←→    Data+",
                "USB D-               ←→    Data-",
                "5V (Pin 18)         ←→    USB Power",
                "GND (Pin 16)        ←→    USB Ground",
                "",
                "USB 2.0 Full Speed (12 Mbps)"
            ])
        
        return "\n".join(diagram)
    
    def get_pin_info(self, pin_number: int) -> Optional[str]:
        """Gibt detaillierte Informationen zu einem spezifischen Pin zurück"""
        return self.flipper_gpio_pins.get(pin_number)
    
    def list_available_connections(self) -> List[str]:
        """Listet alle verfügbaren Verbindungstypen auf"""
        return [conn_type.value for conn_type in ConnectionType]
    
    def generate_full_pinout_reference(self) -> str:
        """Generiert eine vollständige Pin-Referenz"""
        reference = []
        reference.append("╔" + "═" * 58 + "╗")
        reference.append("║" + "Flipper Zero GPIO Komplette Pin-Referenz".center(58) + "║")
        reference.append("╠" + "═" * 58 + "╣")
        
        for pin, description in self.flipper_gpio_pins.items():
            line = f"║ Pin {pin:2d}: {description:<46} ║"
            reference.append(line)
        
        reference.append("╠" + "═" * 58 + "╣")
        reference.append("║" + "Wichtige Hinweise:".ljust(58) + "║")
        reference.append("║" + "• GPIO Spannung: 3.3V (5V NICHT tolerant!)".ljust(58) + "║")
        reference.append("║" + "• Max. Strom pro Pin: 20mA".ljust(58) + "║") 
        reference.append("║" + "• SWD Pins für Debugging verwenden".ljust(58) + "║")
        reference.append("║" + "• VCC ist 3.3V Ausgang (max. 100mA)".ljust(58) + "║")
        reference.append("╚" + "═" * 58 + "╝")
        
        return "\n".join(reference)


def main():
    """Hauptfunktion für Kommandozeilen-Interface"""
    generator = PinoutGenerator()
    
    if len(sys.argv) < 2:
        print("Usage: python pinout_generator.py <connection_type>")
        print("Available connection types:", ", ".join(generator.list_available_connections()))
        print("\nOr use 'full' for complete pin reference")
        return
    
    connection_arg = sys.argv[1].lower()
    
    if connection_arg == "full":
        print(generator.generate_full_pinout_reference())
        return
    
    try:
        connection_type = ConnectionType(connection_arg)
        print(generator.generate_ascii_pinout(connection_type))
        print(generator.generate_connection_diagram(connection_type))
    except ValueError as e:
        print(f"Fehler: {e}")
        print("Verfügbare Verbindungstypen:", ", ".join(generator.list_available_connections()))


if __name__ == "__main__":
    main()
