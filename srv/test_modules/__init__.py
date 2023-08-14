# TODO: SPDX, license info
from . import httpt
from . import ssvplwc
from . import tcpt

modules = {
    #"ping": ping.ping_t,
    "http": httpt.http_t,
    "ssvplwc": ssvplwc.ssvplwc_t,
    "tcp": tcpt.tcp_t
}

try:
    from . import ping
    modules["ping"] = ping.ping_t
except ModuleNotFoundError:
    print("ping module not supported!")


# bool 0: status report
# bool 1: was skipped
def run_test(srv: dict) -> (bool, bool):
    try:
        return modules[srv["module"]](srv), False
    except KeyError:
        print("ssvp: skipping unknown module", srv["module"])
        return None, True
