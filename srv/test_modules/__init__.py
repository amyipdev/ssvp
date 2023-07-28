from . import ping
from . import httpt
from . import ssvplwc
from . import tcpt

modules = {
    "ping": ping.ping_t,
    "http": httpt.http_t,
    "ssvplwc": ssvplwc.ssvplwc_t,
    "tcp": tcpt.tcp_t
}


def run_test(srv: dict) -> bool:
    try:
        return modules[srv["module"]](srv)
    except KeyError:
        print("ssvp: skipping unknown module", srv["module"])
        return None
