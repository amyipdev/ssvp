#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
# 
# ssvp: server statistics viewer project
# Copyright (C) 2023 Amy Parker <amy@amyip.net>
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA or visit the
# GNU Project at https://gnu.org/licenses. The GNU Affero General Public
# License version 3 is available at, for your convenience,
# https://www.gnu.org/licenses/agpl-3.0.en.html. 

from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, Response

import json
import os
import datetime
import socket

import getdb

app = Flask(__name__, template_folder="../web")
cd = os.path.dirname(__file__)
config = json.load(open(x if (x := os.getenv("SSVP_CONFIG")) else f"{cd}/ssvp-config.json", "r"))
if "port" not in config:
    config["port"] = 80 if config["ssl"] is None else 443
if "hostname" not in config:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(0)
    med = None
    try:
        sock.connect(("255.255.255.254", 1))
        med = sock.getsockname()[0]
    except:
        med = "localhost"
    config["hostname"] = f"http{'s' if config['ssl'] is not None else ''}://{med}{':' + str(config['port']) if config['port'] not in (80, 443) else ''}"
db = getdb.get_handler(config["database"])
releaseinfo = json.load(open(f"{cd}/../release-info.json"))


@app.route("/")
@app.route("/status/")
def index():
    return render_template("index.html", config=config, site="index")


@app.route("/credits/")
def r_credits():
    return render_template("credits.html", config=config, site="credits", SSVP_VERSION=releaseinfo["version"])


@app.route("/events/")
def r_events():
    return render_template("events.html", config=config, site="events")


@app.route("/contact/")
def r_contact():
    return render_template("contact.html", config=config, site="contact")


if config.get("docs") == "local":
    @app.route("/docs/")
    def docsbase():
        return redirect("/docs/index.html", code=301)


    @app.route("/docs/<path:path>")
    def docspath(path: str):
        return send_from_directory("../docs/_build/html/", path)


@app.route("/feed.rss")
def fetch_rss():
    return Response(render_template("feed.rss", config=config, evs=db.fetch_events(int(request.args.get("lim", 30)), 0)), mimetype="application/rss+xml")


@app.route("/feed.atom")
def fetch_atom():
    return Response(render_template("feed.atom", config=config, evs=db.fetch_events(int(request.args.get("lim", 30)), 0)), mimetype="application/atom+xml")


@app.route("/assets/<path:path>")
def assets(path: str):
    return send_from_directory("../assets/", path)


@app.route("/api/v1/servers/")
def api_v1_list_servers():
    return jsonify(list(config["servers"].keys()))


@app.route("/api/v1/services/")
def api_v1_services():
    return jsonify(list(config["services"].keys()))


@app.route("/api/v1/uptime_raw/<srv>/")
def api_v1_uptime_raw(srv: str):
    return jsonify(db.get_uptime_stats(srv))


@app.route("/api/v1/uptime/<srv>/")
def api_v1_uptime(srv: str):
    base = db.get_uptime_stats(srv)
    base["daily_types"] = db.get_daily_data(srv)
    return jsonify(base)


@app.route("/api/v1/ctz_date/")
def api_v1_ctz_date():
    return str(datetime.date.today())


@app.route("/api/v1/events/")
def api_v1_events():
    return jsonify(db.fetch_events(int(request.args.get("lim", 100)), int(request.args.get("page", 0))))


@app.route("/api/v1/size/events/")
def api_v1_size_events():
    return jsonify(db.size_events())


# If not run using `flask run`, we can pull options from the config file
if __name__ == "__main__":
    app.run(host="::" if config["enable_host_ipv6"] else "0.0.0.0",
            port=config["port"],
            ssl_context=tuple(config["ssl"]) if type(config["ssl"]) is list else config["ssl"])
