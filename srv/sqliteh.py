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

import dbhandle
import sqlite3
import datetime


class SQLite3Handler(dbhandle.DBAPIAbstracted):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config, prefix=config["prefix"])
        self.filename = config["host"]
        
    def _generate_connection(self):
        # TODO: have filename search the current directory, not the cwd
        return sqlite3.connect(self.filename)
    
    def _treat_sql(self, sql: str):
        return sql.replace("%s", "?")

    def _fetch_daily_data(self, srv: str) -> dict:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"select logDate, serverStatus \
                from {self.p}day_logs \
                where logDate > date('now', '-3 months')\
                    and serverName = ?;"
        curr.execute(sql, (srv,))
        res = {}
        for row in curr.fetchall():
            res[datetime.datetime.strptime(row[0], "%Y-%m-%d").date()] = row[1]
        curr.close()
        conn.close()
        return res

    # TODO: pre-treat instead of live-treating this sql
    def update_cached_stats(self, srv: str, st: int) -> None:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"update {self.p}cached_stats \
                set monthlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate > datetime('now', '-1 month') \
                        and serverName = %s), \
                    yearlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate > datetime('now', '-1 year') \
                        and serverName = %s), \
                    allTimeUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where serverName = %s), \
                    currentStatus = %s\
                where serverName = %s;"
        curr.execute(self._treat_sql(sql), (srv, srv, srv, st, srv))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()
