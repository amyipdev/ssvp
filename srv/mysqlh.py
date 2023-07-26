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


class MySQLHandler(dbhandle.DBAPIAbstracted):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config, prefix=config["prefix"])
        self.host = config["host"]
        self.port = config["port"]
        self.login = config["username"]
        self.pw = config["password"]
        self.db = config["database"]
    
    def get_uptime_stats(self, srv: str) -> dict:
        return self._get_ups(srv=srv, conn=self._generate_connection())
            
    def _generate_connection(self):
        return mysql.connector.connect(user=self.login,
                                       password=self.pw,
                                       host=self.host,
                                       database=self.db)
    
    def _fetch_daily_data(self, srv: str) -> dict:
        return self._fdd(srv=srv, conn=self._generate_connection())

    def handle_daily_record(self, srv: str, st: int) -> int:
        return self._hdr(srv=srv, st=st, conn=self._generate_connection())

    def insert_interval_log(self, srv: str, status: int) -> None:
        self._iil(srv=srv, status=status, conn=self._generate_connection())
        
    def update_cached_stats(self, srv: str, st: int) -> None:
        self._ucs(srv=srv, st=st, conn=self._generate_connection())
