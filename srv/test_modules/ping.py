import ping3


def ping_t(srv: dict) -> bool:
    return bool(ping3.ping(srv["ip"]))
