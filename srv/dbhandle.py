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

import datetime


def unimplemented():
    raise Exception("ssvp: error: db module tried to use an unimplemented function")
    

class DBAbstract:
    def __init__(self, config: dict) -> None:
        pass
    
    def get_uptime_stats(self, srv: str) -> dict:
        unimplemented()
        return {}
    
    def get_daily_data(self, srv: str) -> list:
        base = self._fetch_daily_data(srv)
        res = []
        for z in [datetime.date.today() - datetime.timedelta(days=n) for n in range(89, -1, -1)]:
            if z in base:
                res.append(base[z])
            else:
                res.append(-1)
        return res
    
    def _fetch_daily_data(self, srv: str) -> dict:
        unimplemented()
        return {}
    
    def handle_daily_record(self, srv: str, st: int) -> int:
        unimplemented()
        return 0
        
    def insert_interval_log(self, srv: str, status: int) -> None:
        unimplemented()
        
    def update_cached_stats(self, srv: str, st: int) -> None:
        unimplemented()


# TODO: create a database of pre-treated SQL on initialization
class DBAPIAbstracted(DBAbstract):
    def __init__(self, config: dict, prefix: str) -> None:
        super().__init__(config=config)
        self.p = prefix

    def _generate_connection(self):
        unimplemented()

    def _treat_sql(self, sql: str) -> str:
        return sql

    def _fetch_daily_data(self, srv: str) -> dict:
        return self._fdd(srv=srv, conn=self._generate_connection())

    def handle_daily_record(self, srv: str, st: int) -> int:
        return self._hdr(srv=srv, st=st, conn=self._generate_connection())

    def insert_interval_log(self, srv: str, status: int) -> None:
        self._iil(srv=srv, status=status, conn=self._generate_connection())

    def update_cached_stats(self, srv: str, st: int) -> None:
        self._ucs(srv=srv, st=st, conn=self._generate_connection())

    def get_uptime_stats(self, srv: str) -> dict:
        return self._ups(srv=srv, conn=self._generate_connection())

    def _ups(self, srv: str, conn) -> dict:
        curr = conn.cursor()
        sql = f"select monthlyUptime, yearlyUptime, allTimeUptime, currentStatus \
                from {self.p}cached_stats \
                where serverName = %s;"
        curr.execute(self._treat_sql(sql), (srv,))
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

    def _fdd(self, srv: str, conn) -> dict:
        curr = conn.cursor()
        sql = f"select logDate, serverStatus \
                from {self.p}day_logs \
                where logDate between (current_date() - interval 3 month) and current_date() and serverName = %s;"
        curr.execute(self._treat_sql(sql), (srv,))
        res = {}
        for row in curr.fetchall():
            res[row[0]] = row[1]
        curr.close()
        conn.close()
        return res

    def _hdr(self, srv: str, st: int, conn) -> int:
        curr = conn.cursor()
        day = datetime.date.today()
        sql = f"select exists( \
                    select serverName \
                    from {self.p}day_logs \
                    where serverName = %s \
                        and logDate = %s \
                );"
        curr.execute(self._treat_sql(sql), (srv, day))
        rc_exists = curr.fetchone()[0]
        sql = f"select max( \
                    select severity \
                    from {self.p}events \
                    where serverName = %s \
                        and endTime is not null \
                );"
        mx = None
        try:
            curr.execute(self._treat_sql(sql), (srv,))
            mx = max(st, curr.fetchone()[0])
        # we can ignore the pep violation\
        # in the future, maybe add the type
        except:
            mx = st
        if not rc_exists:
            sql = f"insert into {self.p}day_logs \
                    (logDate, serverName, serverStatus) values \
                    (%s, %s, %s);"
            curr.execute(self._treat_sql(sql), (day, srv, mx))
        else:
            sql = f"select serverStatus \
                    from {self.p}day_logs \
                    where logDate = %s \
                        and serverName = %s;"
            curr.execute(self._treat_sql(sql), (day, srv))
            mx = max(st, curr.fetchone()[0])
            sql = f"update {self.p}day_logs \
                    set serverStatus = %s \
                    where logDate = %s \
                        and serverName = %s;"
            curr.execute(self._treat_sql(sql), (mx, day, srv))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()
        return mx

    def _iil(self, srv: str, status: int, conn) -> None:
        curr = conn.cursor()
        sql = f"insert into {self.p}interval_logs \
                (logDate, serverName, serverStatus) values \
                (%s, %s, %s);"
        curr.execute(self._treat_sql(sql), (datetime.datetime.now(), srv, status))
        curr.fetchall()
        conn.commit()
        curr.close()
        conn.close()

    def _ucs(self, srv: str, st: int, conn) -> None:
        curr = conn.cursor()
        sql = f"update {self.p}cached_stats \
                set monthlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate between \
                        (NOW() - interval 1 month) and NOW() \
                        and serverName = %s), \
                    yearlyUptime = \
                    (select AVG(NOT serverStatus) \
                     from {self.p}interval_logs \
                     where logDate between \
                        (NOW() - interval 1 year) and NOW() \
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
