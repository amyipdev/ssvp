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

from flask import Flask, render_template, send_from_directory, jsonify

import json
import os
import datetime

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
    return jsonify(list(config["servers"].keys()))


@app.route("/api/v1/services")
def api_v1_services():
    return jsonify(list(config["services"].keys()))


@app.route("/api/v1/uptime_raw/<srv>")
def api_v1_uptime_raw(srv: str):
    return jsonify(db.get_uptime_stats(srv))


@app.route("/api/v1/uptime/<srv>")
def api_v1_uptime(srv: str):
    base = db.get_uptime_stats(srv)
    base["daily_types"] = db.get_daily_data(srv)
    return jsonify(base)


@app.route("/api/v1/ctz_date")
def api_v1_ctz_date():
    return str(datetime.date.today())


# If not run using `flask run`, we can pull options from the config file
if __name__ == "__main__":
    app.run(host="::" if config["enable_host_ipv6"] else "0.0.0.0",
            port=config["port"] if "port" in config else (80 if config["ssl"] is None else 443),
            ssl_context=tuple(config["ssl"]) if type(config["ssl"]) is list else config["ssl"])
