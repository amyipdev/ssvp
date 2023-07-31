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

# support existing rustup installs
su - $1 -c "which cargo"
if [ $? -ne 0 ]; then
    CARGO_INSTALL="cargo"
fi

su - $1 -c "which crontab"
if [ $? -ne 0 ]; then
    CRONTAB_INSTALL_APT = "cron"
    CRONTAB_INSTALL_DNF = "cronie"
fi

# NOTE: This doesn't work on dual-platform systems (if both, say, apt and dnf are installed)
if [ -f "/usr/bin/apt" ]; then
    apt update
    apt install python3 python3-pip python3-dev python3-venv libpq-dev nodejs npm sass jq make gcc g++ $CARGO_INSTALL tmux $CRONTAB_INSTALL_APT
elif [ -f "/usr/bin/dnf" ]; then
    dnf install python3 python3-pip python3-devel libpq libpq-devel nodejs nodejs-npm jq make gcc gcc-c++ $CARGO_INSTALL tmux $CRONTAB_INSTALL_DNF
elif [ -f "/usr/bin/yum" ]; then
    yum install python3 python3-pip python3-devel libpq libpq-devel nodejs nodejs-npm jq make gcc gcc-c++ $CARGO_INSTALL tmux $CRONTAB_INSTALL_DNF
else
    echo "Unsupported OS for system package autoinstall"
    exit 1
fi