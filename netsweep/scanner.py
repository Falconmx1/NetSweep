import subprocess
import json
import platform

class NetworkScanner:
    def scan(self, target):
        """Escaneo usando SYN/ARP/ICMP según plataforma"""
        system = platform.system()
        if system == "Windows":
            cmd = f"nmap -sn {target}"
        else:
            cmd = f"nmap -sS -sV -O {target}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return self.parse_nmap_output(result.stdout)

    def parse_nmap_output(self, output):
        lines = output.split("\n")
        hosts = []
        for line in lines:
            if "Nmap scan report for" in line:
                ip = line.split()[-1].strip("()")
                hosts.append({"ip": ip, "status": "up"})
        return {"hosts": hosts, "raw_output": output}
