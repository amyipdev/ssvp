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

import os
import json
import multiprocessing

import getdb
import test_modules

cd = os.path.dirname(__file__)
config = json.load(open(x if (x := os.getenv("SSVP_CONFIG")) else f"{cd}/ssvp-config.json", "r"))
db = getdb.get_handler(config["database"])


# TODO: implement services
def handle_servers(srv: tuple):
    r = test_modules.run_test(srv[1])
    if r[1]:
        return 
    st = -1 if r[0] is None else (0 if r[0] else 2)
    if st != -1:
        db.insert_interval_log(srv[0], False if not st else True)
    st = db.handle_daily_record(srv[0], st)
    db.update_cached_stats(srv[0], st)


with multiprocessing.Pool(int(x) if (x := os.getenv("SSVP_THREADS")) else 4 * multiprocessing.cpu_count()) as p:
    p.map(handle_servers, list(config["servers"].items()) + list(config["services"].items()))
