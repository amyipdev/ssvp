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

SASS := npx sass
SASS_OPTIONS := --trace
SASS_SRCS = $(shell find scss/ -name '*.scss')
INSTALLDIR :=
TSC := npx tsc
TSC_OPTIONS := --noEmitOnError --module es2015
OGUSER := $(USER)
VRSN = $(shell jq -j .version release-info.json)

.PHONY: docs

# TODO: automatically compile sass instead of manual

all:
	mkdir -p assets/css assets/js
	$(SASS) scss/custom.scss:assets/css/custom_bootstrap.css $(SASS_OPTIONS)
	$(TSC) $(TSC_OPTIONS) --outDir assets/js js/*.ts
	
simple_building:
	python3 -m venv venv
	venv/bin/pip3 install -r requirements.txt
	npm i
	$(MAKE)

ssvplwc:
	cd srv/ssvplwc; cargo run --release

install:
	mkdir -p $(INSTALLDIR)
	cp -a . $(INSTALLDIR)
	chown -R $(OGUSER):$(OGUSER) $(INSTALLDIR)

clean:
	rm -rf .sass-cache assets node_modules venv docs/_build artifacts/ rpmbuild/ srv/ssvplwc/target

docs:
	make -C docs html

dir_artifacts:
	mkdir artifacts

tar: clean
	$(MAKE) dir_artifacts
	tar --exclude "artifacts" -czf artifacts/ssvp-$(VRSN).tar.gz ../$(shell basename $(shell pwd))

rpm: tar
	mkdir -p rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
	cp artifacts/ssvp-$(VRSN).tar.gz rpmbuild/SOURCES/ssvp-$(VRSN).tar.gz
	sed -e "s/<VERSION>/$(VRSN)/g" ssvp.spec.fmt > rpmbuild/SPECS/ssvp.spec
	cd rpmbuild; rpmbuild --nodebuginfo --define "_topdir $(shell pwd)/rpmbuild" -v -ba SPECS/ssvp.spec