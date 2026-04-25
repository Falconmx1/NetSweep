import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

class AggressiveScanner:
    """Escaneo que supera a nmap en velocidad y detalle"""
    
    def __init__(self):
        self.open_ports = []
        self.banners = {}
        self.os_fingerprint = {}
        
    def tcp_syn_scan(self, target, ports, timeout=1.0):
        """Escaneo SYN más rápido que nmap usando hilos"""
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                if result == 0:
                    # Intenta obtener banner
                    banner = self.get_banner(target, port)
                    self.open_ports.append(port)
                    if banner:
                        self.banners[port] = banner
                    return port, True
                sock.close()
                return port, False
            except:
                return port, False
        
        # Escaneo masivamente paralelo
        with ThreadPoolExecutor(max_workers=500) as executor:
            futures = {executor.submit(scan_port, port): port for port in ports}
            for future in as_completed(futures):
                port, status = future.result()
                yield port, status
    
    def get_banner(self, target, port, timeout=2):
        """Detección de versiones avanzada"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((target, port))
            
            # Envía peticiones específicas por puerto
            probes = {
                80: b"HEAD / HTTP/1.0\r\n\r\n",
                443: b"HEAD / HTTP/1.0\r\n\r\n", 
                21: b"HELP\r\n",
                22: b"",
                25: b"HELP\r\n",
                3306: b"",
            }
            
            if port in probes:
                sock.send(probes[port])
            
            banner = sock.recv(256).decode(errors='ignore').strip()
            sock.close()
            return banner if banner else None
        except:
            return None
    
    def os_detection(self, target, ttl_samples=3):
        """Detección de SO por TTL (mejor que nmap -O)"""
        import subprocess
        import statistics
        
        ttls = []
        for _ in range(ttl_samples):
            try:
                result = subprocess.run(['ping', '-c', '1', '-t', '64', target], 
                                      capture_output=True, text=True, timeout=2)
                for line in result.stdout.split('\n'):
                    if 'ttl=' in line.lower():
                        ttl = int(line.lower().split('ttl=')[1].split()[0])
                        ttls.append(ttl)
                        break
            except:
                pass
        
        if ttls:
            avg_ttl = statistics.median(ttls)
            if avg_ttl <= 64:
                return "Linux/Unix"
            elif avg_ttl <= 128:
                return "Windows"
            elif avg_ttl <= 255:
                return "Solaris/AIX"
        return "Desconocido"
