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
import mysql.connector
import datetime


class MySQLHandler(dbhandle.DBAbstract):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self.host = config["host"]
        self.port = config["port"]
        self.login = config["username"]
        self.pw = config["password"]
        self.db = config["database"]
        self.p = config["prefix"]
    
    def get_uptime_stats(self, srv: str) -> dict:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"select monthlyUptime, yearlyUptime, allTimeUptime, currentStatus \
                from {self.p}cached_stats \
                where serverName = %s;"
        curr.execute(sql, (srv,))
        row = curr.fetchone()
        if row is None:
            curr.close()
            raise Exception("ssvp: mysql: invalid server")
        curr.close()
        conn.close()
        return {
            "monthly_uptime": row[0],
            "yearly_uptime": row[1],
            "alltime_uptime": row[2],
            "current_status": row[3]
        }
            
    def _generate_connection(self):
        return mysql.connector.connect(user=self.login,
                                       password=self.pw,
                                       host=self.host,
                                       database=self.db)
    
    def _fetch_daily_data(self, srv: str) -> dict:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"select logDate, serverStatus \
                from {self.p}day_logs \
                where logDate between (current_date() - interval 3 month) and current_date() and serverName = %s;"
        curr.execute(sql, (srv,))
        res = {}
        for row in curr.fetchall():
            res[row[0]] = row[1]
        curr.close()
        conn.close()
        return res

    def handle_daily_record(self, srv: str, st: int) -> int:
        conn = self._generate_connection()
        curr = conn.cursor()
        day = datetime.date.today()
        sql = f"select exists( \
                    select serverName \
                    from {self.p}day_logs \
                    where serverName = %s \
                        and logDate = %s \
                );"
        curr.execute(sql, (srv, day))
        rc_exists = curr.fetchone()[0]
        sql = f"select max( \
                    select severity \
                    from {self.p}events \
                    where serverName = %s \
                        and endTime is not null \
                );"
        mx = None
        try:
            curr.execute(sql, (srv,))
            mx = max(st, curr.fetchone()[0])
        # mysql errors are internal\
        # we can ignore the pep violation\
        except:
            mx = st
        if not rc_exists:
            sql = f"insert into {self.p}day_logs \
                    (logDate, serverName, serverStatus) values \
                    (%s, %s, %s);"
            curr.execute(sql, (day, srv, mx))
        else:
            sql = f"update {self.p}day_logs \
                    set serverStatus = %s \
                    where logDate = %s \
                        and serverName = %s;"
            curr.execute(sql, (mx, day, srv))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()
        return mx

    def insert_interval_log(self, srv: str, status: int) -> None:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"insert into {self.p}interval_logs \
                (logDate, serverName, serverStatus) values \
                (%s, %s, %s);"
        curr.execute(sql, (datetime.datetime.now(), srv, status))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()
        
    def update_cached_stats(self, srv: str, st: int) -> None:
        conn = self._generate_connection()
        curr = conn.cursor()
        sql = f"update {self.p}cached_stats \
                set monthlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate between \
                        (CURRENT_DATE() - interval 1 month) and CURRENT_DATE() \
                        and serverName = %s), \
                    yearlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate between \
                        (CURRENT_DATE() - interval 1 year) and CURRENT_DATE() \
                        and serverName = %s), \
                    allTimeUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where serverName = %s), \
                    currentStatus = %s\
                where serverName = %s;"
        curr.execute(sql, (srv, srv, srv, st, srv))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()
