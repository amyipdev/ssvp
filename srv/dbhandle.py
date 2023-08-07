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
import psycopg2


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

    def init_cs(self, srv: str) -> None:
        unimplemented()

    def fetch_events(self, lim: int, page: int) -> list:
        unimplemented()
        return []

    def size_events(self) -> int:
        unimplemented()
        return 0


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
    
    def init_cs(self, srv: str) -> None:
        return self._ics(srv=srv, conn=self._generate_connection())

    def fetch_events(self, lim: int, page: int) -> list:
        return self._fev(lim=lim, page=page, conn=self._generate_connection())

    def size_events(self) -> int:
        return self._sev(conn=self._generate_connection())

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
            conn.commit()
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
        try:
            curr.fetchall()
        except psycopg2.ProgrammingError:
            pass
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
        try:
            curr.fetchall()
        except psycopg2.ProgrammingError:
            pass
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

    def _ics(self, srv: str, conn) -> None:
        curr = conn.cursor()
        sql = f"insert into {self.p}cached_stats \
                (monthlyUptime, yearlyUptime, allTimeUptime, serverName, currentStatus)\
                values (1.0, 1.0, 1.0, %s, -1);"
        curr.execute(self._treat_sql(sql), (srv,))
        try:
            curr.fetchall()
        except psycopg2.ProgrammingError:
            pass
        conn.commit()
        curr.close()
        conn.close()

    def _fev(self, lim: int, page: int, conn) -> list:
        curr = conn.cursor()
        sql = f"select eventID, serverName, startTime, endTime, severity, eventName, eventDescription \
                from {self.p}events \
                order by \
                    (case \
                        when endTime is null \
                            then 1 \
                        else \
                            0 \
                    end) desc, \
                    startTime desc \
                limit %s,%s;"
        curr.execute(self._treat_sql(sql), (lim*page, lim))
        res = []
        try:
            res = [{
                "eventID": x[0],
                "serverName": x[1],
                "startTime": x[2],
                "endTime": x[3],
                "severity": x[4],
                "eventName": x[5],
                "eventDescription": x[6]
            } for x in curr.fetchall()]
        except psycopg2.ProgrammingError:
            pass
        curr.close()
        conn.close()
        return res

    def _sev(self, conn) -> int:
        curr = conn.cursor()
        sql = f"select count(eventID) \
                from {self.p}events;"
        curr.execute(self._treat_sql(sql))
        res = 0
        try:
            res = curr.fetchone()[0]
        except psycopg2.ProgrammingError:
            pass
        curr.close()
        conn.close()
        return res
