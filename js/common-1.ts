// SPDX-License-Identifier: AGPL-3.0-or-later
//
// ssvp: server statistics viewer project
// Copyright (C) 2023 Amy Parker <amy@amyip.net>
//
// This program is free software; you can redistribute it and/or modify it
// under the terms of the GNU Affero General Public License as published
// by the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful, but
// WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
// See the GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA or visit the
// GNU Project at https://gnu.org/licenses. The GNU Affero General Public
// License version 3 is available at, for your convenience,
// https://www.gnu.org/licenses/agpl-3.0.en.html.

export enum DailyInfo {
    Operational = 0,
    NonCriticalEvent = 1,
    CriticalFailure = 2,
    UnknownStatus = -1
}

export interface ServerInfo {
    monthly_uptime: number;
    yearly_uptime: number;
    alltime_uptime: number;
    current_status: DailyInfo;
    daily_types: Array<DailyInfo>;
}

export function convertFontColor(ss: DailyInfo): string {
    switch (ss) {
        case DailyInfo.Operational:
            return "text-success";
        case DailyInfo.NonCriticalEvent:
            return "text-warning";
        case DailyInfo.CriticalFailure:
            return "text-danger";
        default:
            return "text-body-tertiary";
    }
}
