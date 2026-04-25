import ssl
import socket

def check(target):
    try:
        ctx = ssl.create_default_context()
        sock = socket.socket()
        conn = ctx.wrap_socket(sock, server_hostname=target)
        conn.connect((target, 443))
        version = conn.version()
        return version in ["TLSv1.0", "SSLv3"]
    except:
        return False
