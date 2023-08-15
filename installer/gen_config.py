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

import random
import json
import string
import shutil

config = {}

print("Welcome to the SSVP configuration wizard!\n"
      "This will help you build an SSVP configuration.\n\n"
      "Options are indicated by slashes: a/b/c\n"
      "Default options are indicated by brackets: [a]\n")

config["enable_host_ipv6"] = input("Enable IPv6? [y]/n ") != "n"

if input("Enable SSL? [n]/y ") == "y":
    certtype = None
    while certtype not in ("adhoc", "existing"):
        certtype = input("Certificate type? adhoc/existing ")
    if certtype == "adhoc":
        config["ssl"] = "adhoc"
    else:
        config["ssl"] = [
            input("Path to cert.pem: "),
            input("Path to key.pem: ")
        ]
else:
    config["ssl"] = None

if (x := input("Server port number (leave blank to autodetect): ")) != "":
    config["port"] = int(x)
    
config["instance_name"] = input("Name of SSVP instance: ")

if (x := input("Splash text (leave blank for no splash): ")) != "":
    config["splash"] = x

for srvtype in ("servers", "services"):
    config[srvtype] = {}
    inp = ""
    while True:
        inp = input(f"Input name of {srvtype}, or 'end' to stop: ")
        if inp == "end":
            break
        config[srvtype][inp] = {
            "ip": input("Instance IP address: "),
            "module": input("Detector module (ping/tcp/http/ssvplwc): "),
            "args": input("Arguments for module (usually port number): ")
        }
        print(f"Server {inp} added")

# TODO: update this when services are implemented
# TODO: abstract server logic, since services use the same logic
# TODO: abstract `x if (x := promptstr) != "" else default` syntax
config["database"] = {
    "type": input("Database type (mysql/postgres/sqlite3): "),
    "prefix": x if (x := input("Database prefix [ssvp_]: ")) != "" else "ssvp_"
}
if config["database"]["type"] == "sqlite3":
    config["database"]["host"] = input("Path to sqlite3 database file: ")
if config["database"]["type"] in ("mysql", "postgres"):
    config["database"]["host"] = x if (x := input("Database IP [127.0.0.1]: ")) != "" else "127.0.0.1"
    config["database"]["database"] = x if (x := input("Database name [ssvp]: ")) != "" else "ssvp" 
    config["database"]["username"] = x if (x := input("Database username [ssvp]: ")) != "" else "ssvp"
    config["database"]["password"] = input("Database password: ")
    config["database"]["port"] = int(input("Database port: "))
    
if input("Set up contact info? n/[y] ") != "n":
    config["contact"] = {}
    for n in ("Name", "Mastodon", "GitHub", "Git", "Email"):
        if (x := input("{n}: value/[none] ")) != "":
            config[n.lower()] = x

if input("Use local documentation? y/[n] ") == "y":
    config["docs"] = "local"
else:
    config["docs"] = "pages"

filename = "srv/ssvp-config." + "".join(random.choice(string.hexdigits) for _ in range(8)) + ".json"
json.dump(config, open(filename, "w"), indent=4, separators=(',', ': '))
print(f"\nConfig succesfully printed to srv/{filename}.\n"
      f"When you're ready to use this config, run:\n"
      f"  cp srv/{filename} srv/ssvp-config.json\n\n"
      f"Would you like to do so now? y/[n] ", end="")
if input() == "y":
    shutil.copy2(filename, "srv/ssvp-config.json")
    print("Copied file.")
