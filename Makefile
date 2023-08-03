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

SASS := sass
SASS_OPTIONS :=
SASS_SRCS = $(shell find scss/ -name '*.scss')
INSTALLDIR :=

# TODO: automatically compile sass instead of manual

all:
	mkdir -p assets/css assets/js
	$(SASS) scss/custom.scss:assets/css/custom_bootstrap.css $(SASS_OPTIONS)
	$(MAKE) -C js
	
ssvplwc:
	cd srv/ssvplwc; cargo run --release

install:
	mkdir -p $(INSTALLDIR)
	cp -a . $(INSTALLDIR)
	chown -R $(USER):$(USER) $(INSTALLDIR)