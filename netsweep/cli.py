#!/usr/bin/env python3
import argparse
import sys
from .scanner import NetworkScanner
from .version_detector import VersionDetector
from .vuln_scripts import VulnRunner
from .wifi_scanner import WiFiScanner
from .exporter import Exporter

def main():
    parser = argparse.ArgumentParser(description="NetSweep - Escáner de red avanzado")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando scan
    scan_parser = subparsers.add_parser("scan", help="Escaneo de red")
    scan_parser.add_argument("--target", required=True, help="Ej: 192.168.1.0/24")
    scan_parser.add_argument("--output", help="Archivo de salida")
    scan_parser.add_argument("--format", choices=["json", "csv", "html", "pdf"], default="json")

    # Comando versions
    ver_parser = subparsers.add_parser("versions", help="Detección de versiones")
    ver_parser.add_argument("--target", required=True, help="IP o hostname")
    ver_parser.add_argument("--ports", default="21,22,25,80,443,445,3306,5432,8080")

    # Comando vuln
    vuln_parser = subparsers.add_parser("vuln", help="Scripts de vulnerabilidad")
    vuln_parser.add_argument("--target", required=True)
    vuln_parser.add_argument("--script", required=True, help="Nombre del script")

    # Comando wifi
    wifi_parser = subparsers.add_parser("wifi", help="Escaneo WiFi")
    wifi_parser.add_argument("--interface", required=True, help="Interfaz (wlan0, eth0)")

    args = parser.parse_args()

    if args.command == "scan":
        scanner = NetworkScanner()
        results = scanner.scan(args.target)
        if args.output:
            Exporter.export(results, args.output, args.format)
        else:
            print(results)

    elif args.command == "versions":
        detector = VersionDetector()
        results = detector.detect(args.target, args.ports.split(","))
        print(results)

    elif args.command == "vuln":
        runner = VulnRunner()
        result = runner.run(args.target, args.script)
        print(result)

    elif args.command == "wifi":
        wscan = WiFiScanner()
        networks, devices = wscan.scan(args.interface)
        print("Redes encontradas:", networks)
        print("Dispositivos conectados:", devices)

if __name__ == "__main__":
    main()
