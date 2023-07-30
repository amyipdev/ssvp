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

set -e

initialize_mysql() {
    if [ ! -f "/usr/bin/mysql" ]; then
        echo "No MySQL client detected at /usr/bin/mysql"
        exit 1
    fi
    echo -n "Database host: "
    read dbh
    echo -n "Database user (must have *.* with grant option perms): "
    read dbu
    mysql -h $dbh -u $dbu -p < srv/db-setup-mysql.sql
    echo "MySQL succesfully initialized"
}

initialize_postgres() {
    if [ ! -f "/usr/bin/psql" ]; then
        echo "No PostgreSQL client detected at /usr/bin/psql"
        exit 1
    fi
    echo -n "Database host: "
    read dbh
    echo -n "Database username: "
    read dbu
    psql -h $dbh -U $dbu -f srv/db-setup-postgres.sql
    echo "PostgreSQL succesfully initialized"
}

initialize_sqlite3() {
    if [ ! -f "/usr/bin/sqlite3" ]; then
        echo "No SQLite3 client detected at /usr/bin/sqlite3"
        exit 1
    fi
    echo -n "Database file: "
    read dbf
    sqlite3 $dbf < srv/db-setup-sqlite3.sql
    echo "SQLite3 successfully initialized"
}

echo "SSVP Database Wizard"
echo -n "Database type (mysql/postgres/sqlite3): "
read dbt

case $dbt in
    "mysql")
        initialize_mysql
        ;;
    "postgres")
        initialize_postgres
        ;;
    "sqlite3")
        initialize_sqlite3
        ;;
    *)
        echo "Unrecognized database type"
        exit 1
        ;;
esac