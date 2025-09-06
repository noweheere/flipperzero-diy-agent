#!/usr/bin/env python3
"""
FlipperZero DIY Agent - Main Entry Point

Interaktiver Agent für Flipper Zero DIY-Erweiterungen
inklusive Verdrahtung per UART, FTDI, USB und Direktanschluss.

Autor: noweheere
Version: 1.0.0
Lizenz: MIT
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Optional

# Modulstruktur - Platzhalter für zukünftige Module
# TODO: Diese werden in weiteren Commits implementiert
# from modules.pinout import PinoutManager
# from modules.gui import GUIInterface
# from modules.uart import UARTHandler
# from modules.usb import USBHandler
# from modules.ftdi import FTDIHandler

# Projektbasis-Verzeichnis
PROJECT_ROOT = Path(__file__).parent.absolute()

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(PROJECT_ROOT / 'flipper_diy.log')
    ]
)

logger = logging.getLogger('FlipperDIYAgent')


class FlipperDIYAgent:
    """
    Hauptklasse für den DIY Flipper Agent
    
    Verwaltet die verschiedenen Verbindungsmethoden und Module
    für die Interaktion mit Flipper Zero DIY-Erweiterungen.
    """
    
    def __init__(self, connection_type: str = 'auto', debug: bool = False):
        self.connection_type = connection_type
        self.debug = debug
        self.connected = False
        
        # Logging-Level setzen
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
            logger.debug("Debug-Modus aktiviert")
        
        logger.info(f"FlipperDIYAgent initialisiert mit Verbindungstyp: {connection_type}")
        
        # Module-Platzhalter für zukünftige Implementierung
        # self.pinout_manager = PinoutManager()
        # self.gui = GUIInterface()
        # self.uart_handler = None
        # self.usb_handler = None
        # self.ftdi_handler = None
    
    def detect_connection_type(self) -> str:
        """
        Automatische Erkennung des verfügbaren Verbindungstyps
        
        Returns:
            str: Erkannter Verbindungstyp ('uart', 'usb', 'ftdi', 'none')
        """
        logger.info("Erkenne verfügbare Verbindungsmethoden...")
        
        # TODO: Implementierung der automatischen Erkennung
        # - USB-Geräte scannen
        # - UART-Ports prüfen
        # - FTDI-Adapter suchen
        
        # Platzhalter-Rückgabe
        detected = 'none'
        logger.info(f"Erkannter Verbindungstyp: {detected}")
        return detected
    
    def connect(self) -> bool:
        """
        Verbindung zum Flipper Zero herstellen
        
        Returns:
            bool: True wenn Verbindung erfolgreich
        """
        if self.connection_type == 'auto':
            self.connection_type = self.detect_connection_type()
        
        if self.connection_type == 'none':
            logger.error("Keine gültige Verbindungsmethode verfügbar")
            return False
        
        logger.info(f"Stelle Verbindung her über: {self.connection_type}")
        
        # TODO: Verbindungslogik je nach Typ implementieren
        # if self.connection_type == 'uart':
        #     self.uart_handler = UARTHandler()
        #     self.connected = self.uart_handler.connect()
        # elif self.connection_type == 'usb':
        #     self.usb_handler = USBHandler()
        #     self.connected = self.usb_handler.connect()
        # elif self.connection_type == 'ftdi':
        #     self.ftdi_handler = FTDIHandler()
        #     self.connected = self.ftdi_handler.connect()
        
        # Platzhalter - Verbindung als erfolgreich simulieren
        self.connected = True
        
        if self.connected:
            logger.info("Verbindung erfolgreich hergestellt")
        else:
            logger.error("Verbindung fehlgeschlagen")
        
        return self.connected
    
    def disconnect(self) -> None:
        """
        Verbindung trennen und Ressourcen freigeben
        """
        if self.connected:
            logger.info("Trenne Verbindung...")
            
            # TODO: Handler-spezifische Disconnect-Logik
            # if self.uart_handler:
            #     self.uart_handler.disconnect()
            # if self.usb_handler:
            #     self.usb_handler.disconnect()
            # if self.ftdi_handler:
            #     self.ftdi_handler.disconnect()
            
            self.connected = False
            logger.info("Verbindung getrennt")
    
    def run_interactive_mode(self) -> None:
        """
        Startet den interaktiven Modus des Agents
        """
        print("\n=== FlipperZero DIY Agent - Interaktiver Modus ===")
        print("Verfügbare Befehle:")
        print("  help    - Diese Hilfe anzeigen")
        print("  status  - Verbindungsstatus anzeigen")
        print("  scan    - Nach Geräten scannen")
        print("  connect - Verbindung herstellen")
        print("  disconnect - Verbindung trennen")
        print("  gui     - GUI-Modus starten (geplant)")
        print("  exit    - Programm beenden")
        print()
        
        while True:
            try:
                cmd = input("flipper-diy> ").strip().lower()
                
                if cmd in ['exit', 'quit', 'q']:
                    break
                elif cmd == 'help':
                    print("Verfügbare Befehle: help, status, scan, connect, disconnect, gui, exit")
                elif cmd == 'status':
                    status = "Verbunden" if self.connected else "Nicht verbunden"
                    print(f"Status: {status} (Typ: {self.connection_type})")
                elif cmd == 'scan':
                    detected = self.detect_connection_type()
                    print(f"Erkannte Verbindung: {detected}")
                elif cmd == 'connect':
                    if self.connect():
                        print("Verbindung erfolgreich hergestellt")
                    else:
                        print("Verbindung fehlgeschlagen")
                elif cmd == 'disconnect':
                    self.disconnect()
                    print("Verbindung getrennt")
                elif cmd == 'gui':
                    print("GUI-Modus wird in einem zukünftigen Commit implementiert...")
                elif cmd == '':
                    continue
                else:
                    print(f"Unbekannter Befehl: {cmd}. Verwenden Sie 'help' für Hilfe.")
                    
            except KeyboardInterrupt:
                print("\nBeende...")
                break
            except EOFError:
                break
        
        self.disconnect()
        print("Auf Wiedersehen!")


def create_arg_parser() -> argparse.ArgumentParser:
    """
    Erstellt und konfiguriert den Argument-Parser
    
    Returns:
        argparse.ArgumentParser: Konfigurierter Parser
    """
    parser = argparse.ArgumentParser(
        description='FlipperZero DIY Agent - Interaktiver Agent für DIY-Erweiterungen',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Verbindungstypen:
  auto      - Automatische Erkennung (Standard)
  uart      - UART-Verbindung
  usb       - USB-Verbindung
  ftdi      - FTDI-Adapter
  direct    - Direktanschluss

Beispiele:
  %(prog)s --interactive
  %(prog)s --connection uart --debug
  %(prog)s --gui
        """
    )
    
    parser.add_argument(
        '--connection', '-c',
        choices=['auto', 'uart', 'usb', 'ftdi', 'direct'],
        default='auto',
        help='Verbindungstyp zum Flipper Zero (Standard: auto)'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Startet den interaktiven Modus'
    )
    
    parser.add_argument(
        '--gui', '-g',
        action='store_true',
        help='Startet die grafische Benutzeroberfläche (geplant)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Aktiviert Debug-Ausgaben'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='FlipperZero DIY Agent v1.0.0'
    )
    
    return parser


def main() -> int:
    """
    Hauptfunktion - Entry Point des Programms
    
    Returns:
        int: Exit-Code (0 = Erfolg, 1 = Fehler)
    """
    try:
        parser = create_arg_parser()
        args = parser.parse_args()
        
        # FlipperDIYAgent initialisieren
        agent = FlipperDIYAgent(
            connection_type=args.connection,
            debug=args.debug
        )
        
        # Modus basierend auf Argumenten bestimmen
        if args.gui:
            print("GUI-Modus wird in einem zukünftigen Commit implementiert...")
            # TODO: GUI starten
            # agent.gui.start()
            return 0
        elif args.interactive or len(sys.argv) == 1:
            # Interaktiver Modus (Standard wenn keine Argumente)
            agent.run_interactive_mode()
            return 0
        else:
            # Andere Modi können hier hinzugefügt werden
            parser.print_help()
            return 0
            
    except KeyboardInterrupt:
        logger.info("Programm durch Benutzer unterbrochen")
        return 0
    except Exception as e:
        logger.error(f"Unerwarteter Fehler: {e}")
        if args.debug if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    # Skript direkt ausgeführt
    sys.exit(main())
