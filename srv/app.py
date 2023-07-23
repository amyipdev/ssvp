#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory

import json
import os

import getdb

app = Flask(__name__, template_folder="../web")
cd = os.path.dirname(__file__)
config = json.load(open(f"{cd}/ssvp-config.json", "r"))
db = getdb.get_handler(config["database"])


@app.route("/")
@app.route("/status")
def index():
    return render_template("index.html", config=config, site="index")


@app.route("/credits")
def r_credits():
    return render_template("credits.html", config=config, site="credits")


@app.route("/events")
def r_events():
    return render_template("events.html", config=config, site="events")


@app.route("/assets/<path:path>")
def assets(path: str):
    return send_from_directory("../assets/", path)


@app.route("/api/v1/servers")
def api_v1_list_servers():
    return json.dumps(list(config["servers"].keys()))


@app.route("/api/v1/uptime_raw/<srv>")
def api_v1_uptime_raw(srv: str):
    return json.dumps(db.get_uptime_stats(srv))


@app.route("/api/v1/uptime/<srv>")
def api_v1_uptime(srv: str):
    base = db.get_uptime_stats(srv)
    base["daily_types"] = db.get_daily_data(srv)
    return json.dumps(base)


# If not run using `flask run`, we can pull options from the config file
if __name__ == "__main__":
    app.run(host="::" if config["enable_host_ipv6"] else "0.0.0.0", port=config["port"])
