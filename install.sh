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

echo -e "SSVP Setup and Installer\n\nPlease ensure that you are logged in as the user you wish to install SSVP as.\n"

echo -n "Autoinstall system dependencies? (Debian and Fedora derivatives only) y/[n] "
read AILDPDS
if [ "$AILDPDS" == "y" ]; then
    bash -c "$PREROOT installer/autoinstall-deps-system.sh $USER"
else
    echo -n "Verify system dependencies? y/[n] "
    read VFYDPS
    if [ "$VFYDPS" == "y" ]; then
        bash installer/verify-deps-system.sh
    fi
fi

if [ ! -d "venv" ]; then
    echo -n "Create virtual environment? (recommended) n/[y] "
    read CRVENV
    if [ "$CRVENV" != "n" ]; then
        python3 -m venv venv
    fi
fi

if [ "$VIRTUAL_ENV" == "" ]; then
    if [ -d "venv" ]; then
        echo -n "Source detected venv? (recommended) n/[y] "
        read SRVENV
        if [ "$SRVENV" != "n" ]; then
            source venv/bin/activate
        fi
    fi
fi

echo -n "Install PyPI dependencies? n/[y] "
read INSPYPI
if [ "$INSPYPI" != "n" ]; then
    pip3 install -r requirements.txt
fi

echo -n "Install NPM dependencies? n/[y] "
read INSNPM
if [ "$INSNPM" != "n" ]; then
    npm i
fi

echo -n "Compile site dependencies? n/[y] "
read CMPSDP
if [ "$CMPSDP" != "n" ]; then
    make
fi

echo -n "Initialize database system for SSVP? (use defaults when generating configuration) y/[n] "
read INIDBS
if [ "$INIDBS" == "y" ]; then
    bash installer/initialize-databases.sh
    echo "For mysql and postgres: make sure to change the database password after finishing install/setup."
fi

echo -n "Generate ssvp config file? n/[y] "
read GENCF
if [ "$GENCF" != "n" ]; then
    python3 installer/gen_config.py
fi

echo -n "Initialize the cached statistics table? n/[y] "
read INISCS
if [ "$INISCS" != "n" ]; then
    python3 srv/initialized_cached_stats.py
fi

echo -n "Would you like to run the full installation now? n/[y] "
read CONTINS
if [ "$CONTINS" == "n" ]; then
    echo "Existing SSVP installation wizard. Remember to set up cron jobs."
    exit 0
fi

echo -n "Installation directory [current directory]: "
read INSDIR
if [ "$INSDIR" != "" ]; then
    $PREROOT make install INSTALLDIR=$INSDIR OGUSER=$(whoami)
    # handle SELinux
    if [ -f "/usr/sbin/restorecon" ]; then
        $PREROOT restorecon -rv $INSDIR
    fi
else
    INSDIR="$(pwd)"
fi

# TODO: switch to case
echo -n "Choose an autorunner method (systemd/cron/[none]): "
read ATRMTH
if [ "$ATRMTH" == "cron" ]; then
    (crontab -l; echo "*/5 * * * * $INSDIR/venv/bin/python3 $INSDIR/srv/interval.py") | crontab -
    echo "Cron runner installed"
elif [ "$ATRMTH" == "systemd" ]; then
    for i in ssvp-gunicorn.service ssvp-werkzeug.service; do
        sed -e "s/<INSTALLDIR>/$(echo $INSDIR | sed 's_/_\\/_g')/g" srv/systemd/$i | $PREROOT tee $INSDIR/srv/systemd/$i > /dev/null
        $PREROOT ln -sf $INSDIR/srv/systemd/$i /usr/lib/systemd/system/$i
    done
    $PREROOT systemctl daemon-reload
    echo -n "Enable on boot? prod/dev/[none] "
    read ATRACN
    case $ATRACN in
        "prod")
            $PREROOT systemctl enable --now ssvp-gunicorn.service
            ;;
        "dev")
            $PREROOT systemctl enable --now ssvp-werkzeug.service
            ;;
        *)
            echo "To load on boot or start SSVP later, read https://ssvp.docs.amyip.net/configuration.html#systemd"
            ;;
    esac
fi

# TODO: switch to case
echo -n "Choose a server reboot launch method (systemd/cron/[none]): "
read RBTLNC
if [ "$RBTLNC" == "cron" ]; then
    (crontab -l; echo "@reboot $INSDIR/srv/tmux.sh") | crontab -
elif [ "$RBTLNC" == "systemd" ]; then
    for i in ssvp-interval.service ssvp-interval.timer; do
        sed -e "s/<INSTALLDIR>/$(echo $INSDIR | sed 's_/_\\/_g')/g" srv/systemd/$i | $PREROOT tee $INSDIR/srv/systemd/$i > /dev/null
        $PREROOT ln -sf $INSDIR/srv/systemd/$i /usr/lib/systemd/system/$i
    done
    $PREROOT systemctl daemon-reload
    echo -n "Enable timer now? n/[y] "
    read ENATIM
    if [ "$ENATIM" != "n" ]; then
        $PREROOT systemctl enable --now systemctl-interval.timer
    else
        echo "Timer loading information available at https://ssvp.docs.amyip.net/configuration.html#systemd"
    fi
fi

echo "Installation finished."