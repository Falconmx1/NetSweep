import requests

def check(target):
    try:
        r = requests.get(f"http://{target}", auth=("admin", "admin"), timeout=3)
        return r.status_code == 200
    except:
        return False
