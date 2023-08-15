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

import {convertFontColor, DailyInfo} from "./common-1.js";

interface EventListing {
    eventID: number;
    serverName: string;
    startTime: Date;
    endTime: Date;
    severity: DailyInfo;
    eventName: string;
    eventDescription: string;
}

const LIM_PER_PAGE: number = 5;

let eventsList: Array<EventListing>;
let currPage: number = 0;
let numPages: number;
const leftHandler = document.getElementById("pg-bt-left");
const rightHandler = document.getElementById("pg-bt-right");

async function fetchEventsList(page: number) {
    if (typeof numPages === "undefined") {
        const r = await fetch("/api/v1/size/events");
        numPages = Math.ceil((parseInt(await r.text())) / LIM_PER_PAGE) - 1;
        console.log(numPages);
    }
    if (typeof eventsList === "undefined" || page != currPage) {
        currPage = page;
        const r = await fetch(`/api/v1/events?lim=${LIM_PER_PAGE}&page=${page}`);
        eventsList = await r.json();
        for (let i = 0; i < eventsList.length; ++i) {
            eventsList[i].startTime = new Date(eventsList[i].startTime);
            if (eventsList[i].endTime != null)
                eventsList[i].endTime = new Date(eventsList[i].endTime);
        }
        if (page != 0)
            leftHandler.classList.remove("disabled");
        else
            leftHandler.classList.add("disabled");
        if (page < numPages)
            rightHandler.classList.remove("disabled");
        else
            rightHandler.classList.add("disabled");
    }
    generateEventsTable();
}

document.getElementById("pg-bt-left");

fetchEventsList(0);

function translateDailyInfo(src: DailyInfo): string {
    switch (src) {
        case DailyInfo.Operational:
            return "Informational";
        case DailyInfo.NonCriticalEvent:
            return "Non-Critical&nbsp;Event";
        case DailyInfo.CriticalFailure:
            return "Critical&nbsp;Event";
        default:
            return "Unknown Severity";
    }
}

function generateEventsTable(): void {
    let builder: string = `<div class="table-responsive">
                                <table class="table" id="events-table">`;
    for (let sp: number = 0; sp < eventsList.length; ++sp) {
        const ev: EventListing = eventsList[sp];
        builder += `<tr>
                        <th class="bg-body-tertiary rounded-4 py-3 px-4 ${ev.endTime == null ? "border-2 border-warning-subtle" : ""}">
                            <table class="unpadded-table">
                                <tr class="bg-body-tertiary border-0">
                                    <th class="half-width bg-body-tertiary border-0">${ev.eventName}</th>
                                    <th class="half-width bg-body-tertiary ${convertFontColor(ev.severity)} text-end border-0">${translateDailyInfo(ev.severity)}</th>
                                </tr>
                            </table>
                            <div class="container-fluid bg-body-secondary py-2 my-2 rounded-4">
                                <p class="m-2">${ev.eventDescription}</p>
                            </div>
                            <table class="unpadded-table">
                                <tr class="bg-body-tertiary border-0">
                                    <th class="half-width bg-body-tertiary border-0">${ev.serverName}</th>
                                    <th class="half-width bg-body-tertiary text-end border-0">
                                        ${ev.startTime.getUTCFullYear()}/${ev.startTime.getUTCMonth()}/${ev.startTime.getUTCDate()} -
                                        ${ev.endTime == null ? "now" : `${ev.endTime.getUTCFullYear()}/${ev.endTime.getUTCMonth()}/${ev.endTime.getUTCDate()}`}
                                    </th>
                                </tr>                                                                                                                                 
                            </table>
                        </th>
                    </tr>`;
    }
    builder += `    </table>
                </div>`;
    document.getElementById("events-table-gen").innerHTML = builder;
}

leftHandler.addEventListener("click", () => {fetchEventsList(currPage-1);});
rightHandler.addEventListener("click", () => {fetchEventsList(currPage+1);});