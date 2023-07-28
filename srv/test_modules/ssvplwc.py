import socket


def ssvplwc_t(srv: dict) -> bool:
    try:
        ss = socket.socket()
        ss.connect((srv["ip"], int(srv["args"])))
        b = ss.recv(2048)
        return b == b"ssvp-ok"
    except ConnectionError:
        return False
