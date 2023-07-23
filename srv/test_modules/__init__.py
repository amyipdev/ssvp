from . import ping

modules = {
    "ping": ping.ping_t
}


def run_test(srv: dict) -> bool:
    try:
        return modules[srv["module"]](srv)
    except KeyError:
        print("ssvp: skipping unknown module", srv["module"])
        return None
