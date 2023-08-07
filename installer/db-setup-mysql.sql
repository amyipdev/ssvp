-- SPDX-License-Identifier: AGPL-3.0-or-later
--
-- ssvp: server statistics viewer project
-- Copyright (C) 2023 Amy Parker <amy@amyip.net>
--
-- This program is free software; you can redistribute it and/or modify it
-- under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation; either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful, but
-- WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
-- See the GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program; if not, write to the Free Software Foundation, Inc.,
-- 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA or visit the
-- GNU Project at https:--gnu.org/licenses. The GNU Affero General Public
-- License version 3 is available at, for your convenience,
-- https:--www.gnu.org/licenses/agpl-3.0.en.html. 

create database ssvp;
grant all privileges on ssvp.* to 'ssvp'@'%' identified by 'ssvp-demo';
use ssvp;
create table ssvp_day_logs (logDate date not null, serverName text not null, serverStatus integer not null);
create table ssvp_interval_logs (logDate datetime not null, serverName text not null, serverStatus boolean not null);
create table ssvp_cached_stats (monthlyUptime double not null, yearlyUptime double not null, allTimeUptime double not null, serverName text not null, currentStatus integer not null);
create table ssvp_events (eventID integer not null auto_increment, serverName text not null, eventName text not null, eventDescription text, startTime datetime not null, endTime datetime, severity integer not null, primary key (eventID);