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

which jq
if [ $? -ne 0 ]; then
    echo "jq not found"
    exit 1
fi

set -e

cd "$(dirname "$0")"

if [ "$SSVP_CONFIG" == "" ]; then
    SSVP_CONFIG=ssvp-config.json
fi

SSL=$(jq -j .ssl $SSVP_CONFIG)
PORT=$(jq -j .port $SSVP_CONFIG)

if [ $PORT == "null" ]; then
    if [ $SSL != "null" ]; then
        PORT=443
    else
        PORT=80
    fi
fi

if [ $SSL == "adhoc" ]; then
    echo "Adhoc certs not supported for Gunicorn"
    exit 1
fi

if [ $SSL != "null" ]; then
    SSLARGS=" --certfile $(jq -j .ssl[0]) --keyfile $(jq -j .ssl[1]) "
fi

if [ $(jq -j .enable_host_ipv6 ssvp-config.json) != "true" ]; then
    BINDADDR="0.0.0.0:$PORT"
else
    BINDADDR="[::]:$PORT"
fi

if [ "$SSVP_THREADS" == "" ]; then
    SSVP_THREADS=$(( 2 * $(nproc) ))
fi

gunicorn -w $SSVP_THREADS 'app:app' -b $BINDADDR $SSLARGS