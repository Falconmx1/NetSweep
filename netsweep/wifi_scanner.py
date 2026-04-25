import subprocess
import re

class WiFiScanner:
    def scan(self, interface):
        if platform.system() == "Linux":
            output = subprocess.run(["sudo", "iwlist", interface, "scan"], capture_output=True, text=True).stdout
            networks = re.findall(r'ESSID:"(.+?)"', output)
            return networks, []
        else:
            # Windows: netsh wlan show networks
            output = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True).stdout
            networks = re.findall(r"SSID \d+ : (.+)", output)
            return networks, []
