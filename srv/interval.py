import os
import json
import multiprocessing

import getdb
import test_modules

cd = os.path.dirname(__file__)
config = json.load(open(f"{cd}/ssvp-config.json", "r"))
db = getdb.get_handler(config["database"])


# TODO: implement services
def handle_servers(srv: tuple):
    r = test_modules.run_test(srv[1])
    st = -1 if r is None else (0 if r else 2)
    if st != -1:
        db.insert_interval_log(srv[0], False if not st else True)
    st = db.handle_daily_record(srv[0], st)
    db.update_cached_stats(srv[0], st)


with multiprocessing.Pool(8) as p:
    p.map(handle_servers, config["servers"].items())
