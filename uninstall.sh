#!/usr/bin/bash
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

cd "$(dirname "$0")"

echo "SSVP Uninstaller - cleanly uninstalls SSVP"

if [ $(id -u) -ne 0 ]; then
    which sudo > /dev/null
    if [ $? -ne 0 ]; then
        which doas > /dev/null
        if [ $? -ne 0 ]; then
            echo "Either run as root, or have sudo installed"
            exit 1
        else
            PREROOT="doas"
        fi
    else
        PREROOT="sudo"
    fi
fi

echo -n "Installation directory: [none] "
read INSDIR
if [ "$INSDIR" != "" ]; then
    $PREROOT rm -rf $INSDIR
fi

which systemctl > /dev/null
if [ $? -eq 0 ]; then
    echo -n "Clear systemd? n/[y] "
    read CLRSMD
    if [ "$CLRSMD" != "n" ]; then
        set +e
        for i in ssvp-gunicorn.service ssvp-interval.service ssvp-interval.timer ssvp-werkzeug.service; do
            # --now was causing systemctl to hang, so do it manually
            $PREROOT systemctl disable $i
            $PREROOT systemctl stop $i
            $PREROOT rm -f /usr/lib/systemd/system/$i
        done
        set -e
    fi
fi

echo "Uninstall complete."