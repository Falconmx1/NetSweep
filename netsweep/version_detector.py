import socket
import ssl

class VersionDetector:
    def detect(self, target, ports):
        results = {}
        for port in ports:
            port = int(port)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target, port))
                banner = sock.recv(1024).decode(errors="ignore").strip()
                results[port] = {"service": self.guess_service(port), "banner": banner}
                sock.close()
            except:
                results[port] = {"service": self.guess_service(port), "banner": "Closed/Filtered"}
        return results

    def guess_service(self, port):
        services = {21: "FTP", 22: "SSH", 25: "SMTP", 80: "HTTP", 443: "HTTPS", 445: "SMB", 3306: "MySQL"}
        return services.get(port, "Unknown")
