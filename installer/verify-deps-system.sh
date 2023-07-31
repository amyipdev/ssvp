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

# LIMITATION: We can't actually really check for libpq-dev(el).
# It could technically be installed *anywhere* with some tricks.
# Same goes for python3-dev(el). Let's just presume it's installed,
# setup.py will fail if things go wrong anyways...

if [ ! -f "/usr/bin/pip3" ]; then
    echo "No system pip3 detected"
    exit 1
fi

declare -a deps=( "python3" "jq" "gcc" "g++" "cargo" "tmux" "npx" "npm" "crontab" )

for dep in "${deps[@]}"
do
    which $dep
    if [ $? -ne 0 ]; then
        echo "Missing required dependency $dep"
        exit 1
    fi
done