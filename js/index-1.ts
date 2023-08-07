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

import { DailyInfo, ServerInfo, convertFontColor } from "./common-1.js";

const EXPANSION_SIZE: number = 1280;
const SINGLE_MONTH_SHIFT: number = 800;
const DOUBLE_MONTH_SHIFT: number = 1920;
const PCT_BREAKDOWN_SPLIT: number = 720;
const PCT_BREAKDOWN_SPLIT_TWO: number = 1366;
const DSF: number = 5;
const MSD: number = 86400000;
const MONTHS: Array<string> = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

// TODO: internationalization of strings in here
let serverListExpanded: number = getDisplayCategory();
let listOfServers: Array<string>;
let listOfServices: Array<string>;
let serverInfoList: Array<ServerInfo> = [];
let todaysCurrentDate: Date = new Date();
todaysCurrentDate.setUTCHours(0, 0, 0, 0);

async function serverListInitialization() {
    serverInfoList = [];
    if (typeof listOfServers === "undefined") {
        const r = await fetch("/api/v1/servers");
        listOfServers = await r.json();
    }
    if (typeof listOfServices === "undefined") {
        const r = await fetch("/api/v1/services");
        listOfServices = await r.json();
    }
    for (const srv of listOfServers.concat(listOfServices)) {
        const sr = await fetch("/api/v1/uptime/" + srv);
        serverInfoList.push(await sr.json());
    }
    const tr = await fetch("/api/v1/ctz_date");
    const nd: Array<number> = (await tr.text()).split("-").map((x) => parseInt(x));
    todaysCurrentDate.setUTCFullYear(nd[0], nd[1]-1, nd[2]);
    let box: HTMLElement = document.getElementById("totality-indic");
    // when services are implemented,
    // add an && clause for servicesList.every
    let mx: number = 0;
    for (const e of serverInfoList) {
        mx = Math.max(mx, e.current_status);
    }
    switch (mx) {
        case 0:
            box.innerHTML = "All Systems Operational";
            box.classList.add("bg-success");
            break;
        case 1:
            box.innerHTML = "Non-Critical Event";
            box.classList.add("bg-warning");
            break;
        case 2:
            box.innerHTML = "Critical Failure";
            box.classList.add("bg-danger");
            break;
        default:
            box.innerHTML = "(unknown error)";
            box.classList.add("bg-body-tertiary")
    }
    generate_table();
    generate_accordion();
}

serverListInitialization();

function dailyinfo_tostring(di: DailyInfo): string {
    switch (di) {
        case DailyInfo.Operational:
            return "Operational";
        case DailyInfo.CriticalFailure:
            return "Critical&nbsp;Failure";
        case DailyInfo.NonCriticalEvent:
            return "Non-Critical&nbsp;Event";
        case DailyInfo.UnknownStatus:
            return "Unknown&nbsp;Status";
        default:
            return "(site&nbsp;error)";
    }
}

function gen_pct_string(pct: number, sf: number): string {
    return (Math.round(pct * (10**(sf+2))) / (10**sf)).toString() + "%";
}

function generate_table(): void {
    let builder: string = "<table class=\"table\" id=\"instance-table\">";
    let sp: number = 0; // string pointer
    const mc: number = serverListExpanded > 2 ? 2 : 1; // max count per row
    const ll = listOfServers.length;
    const numBars: number = (window.innerWidth < SINGLE_MONTH_SHIFT ? 30 :
                                (window.innerWidth < DOUBLE_MONTH_SHIFT ? 60 : 90));
    const adj: number = 90 - numBars;
    while (sp < ll) {
        builder += "<tr>";
        for (let p: number = 0; p < mc; ++p) {
            if (sp >= ll)
                break;
            // TODO: convert this all into a single backtick string
            const ss: DailyInfo = serverInfoList[sp].current_status;
            builder += `
                <th class="px-4 bg-body-tertiary w-50 rounded-4">
                    <div class="table-responsive">
                        <table class="unpadded-table">
                            <tr class="bg-body-tertiary border-0">
                                <th class="half-width bg-body-tertiary border-0">${listOfServers[sp]}</th>
                                <th class="half-width bg-body-tertiary ${convertFontColor(ss)} text-end border-0">${dailyinfo_tostring(ss)}</th>
                            </tr>
                        </table>
                    </div>
                    <svg class="my-2" preserveAspectRatio="none" viewBox="0 0 ${numBars*5-2} 35">`;
            for (let j: number = 0; j < numBars; ++j) {
                // @ts-ignore
                let d: Date = new Date(todaysCurrentDate - ((numBars-1-j)*MSD));
                builder += `<rect rx="2" class="indic-${serverInfoList[sp].daily_types[j+adj]}" height="35" width="3" x="${5*j}" y="0"></rect>
                            <foreignObject x="${5*j}" y="0" height="35" width="3">
                                <button class="border-0 m-0 p-0" style="background-color: rgba(0, 0, 0, 0%); height: 100%; width: 100%" type="button" data-bs-toggle="popover" data-bs-placement="top" data-bs-trigger="hover"
                                    data-bs-title="${d.getUTCFullYear()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}"
                                    data-bs-content="${dailyinfo_tostring(serverInfoList[sp].daily_types[j+adj])}"></button>
                            </foreignObject>`;
            }
            builder += `
                    </svg>
                    <div class="table-responsive border-0">
                        <table class="unpadded-table border-0">
                            <tr class="bg-body-tertiary border-0">
                                <th class="half-width bg-body-tertiary border-0 pt-0" style="font-size: 0.85rem;">${numBars} days ago</th>
                                <th class="half-width bg-body-tertiary border-0 pt-0 text-end" style="font-size: 0.85rem;">now</th>
                            </tr>
                        </table>
                    </div>
                    <div class="table-responsive border-0">
                        <table class="unpadded-table border-0">
                            <tr class="bg-body-tertiary border-0">`;
            for (const e of [["Monthly", serverInfoList[sp].monthly_uptime],
                             ["Yearly", serverInfoList[sp].yearly_uptime],
                             ["All-time", serverInfoList[sp].alltime_uptime]]) {
                // We can ignore here, because e[1] is guaranteed to be 'number'
                // Would type-annotate e, but we can't, since it's in a for-of
                // TODO: see if there's a way to type-annotate a for-each
                // @ts-ignore
                const pct: number = gen_pct_string(e[1], DSF);
                const inside: string = (window.innerWidth >= PCT_BREAKDOWN_SPLIT)
                                        ?  `<div class="table-responsive border-0">
                                                <table class="unpadded-table border-0">
                                                    <tr class="bg-body-tertiary border-0">
                                                        <th class="half-width bg-body-tertiary border-0"><p class="table-uptime-element text-start">${e[0]}</p></th>
                                                        <th class="half-width bg-body-tertiary border-0"><p class="table-uptime-element text-end">${pct}</p></th>
                                                    </tr>
                                                </table>
                                            </div>`
                                        : `<p class="table-uptime-element text-center">${e[0]}<br>${pct}</p>`;
                builder += `<th class="border-0 bg-body-tertiary">${inside}</th>`;
            }
            builder += `
                            </tr>
                        </table>
                    </div>                                                       
                </th>
            `;
            ++sp;
        }
        builder += "</tr>";
    }
    builder += "</table>";
    document.getElementById("table-gen").innerHTML = builder;
}

function generate_accordion(): void {
    let builder: string = "<div class=\"accordion\" id=\"accordionGen\">";
    let sp: number = listOfServers.length;
    const hd: number = sp;
    const ll: number = serverInfoList.length;
    const numBars: number = (window.innerWidth < SINGLE_MONTH_SHIFT ? 30 :
                                (window.innerWidth < DOUBLE_MONTH_SHIFT ? 60 : 90));
    const adj: number = 90 - numBars;
    while (sp < ll) {
        const ss: DailyInfo = serverInfoList[sp].current_status;
        const rc: string = sp == hd ? "rounded-top-4" : (sp == ll - 1 ? "rounded-bottom-4" : "");
        builder += `<div class="accordion-item ${rc}">
                        <h2 class="accordion-header">
                            <button id="accordbt-${sp}" class="accordion-button bg-body-tertiary ${rc}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${sp}" aria-expanded="true" aria-controls="collapse${sp}">
                                <div class="table-responsive" style="width: 100%">
                                    <table class="unpadded-table border-0">
                                        <tr class="border-0">
                                            <th class="half-width bg-body-tertiary pl-2 border-0">${listOfServices[sp-hd]}</th>
                                            <th style="white-space: nowrap; vertical-align: middle" class="half-width bg-body-tertiary pr-4 border-0 text-end ${convertFontColor(ss)}">${dailyinfo_tostring(ss)}</th>
                                        </tr>
                                    </table>
                                </div>
                            </button>
                        </h2>
                        <div id="collapse${sp}" class="accordion-collapse collapse" data-bs-parent="#accordionGen">
                            <div class="accordion-body">
                                <svg class="my-2" preserveAspectRatio="none" viewBox="0 0 ${numBars*5-2} 15">`;
        for (let j: number = 0; j < numBars; ++j) {
            // @ts-ignore
            let d: Date = new Date(todaysCurrentDate - ((numBars-1-j)*MSD));
            builder += `<rect rx="2" class="indic-${serverInfoList[sp].daily_types[j+adj]}" height="15" width="3" x="${5*j}" y="0"></rect>
                        <foreignObject x="${5*j}" y="0" height="15" width="3">
                            <button class="border-0 m-0 p-0" style="background-color: rgba(0, 0, 0, 0%); height: 500%; width: 100%" type="button" data-bs-toggle="popover" data-bs-placement="top" data-bs-trigger="hover"
                                data-bs-title="${d.getUTCFullYear()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCDate()}"
                                data-bs-content="${dailyinfo_tostring(serverInfoList[sp].daily_types[j+adj])}"></button>
                        </foreignObject>`;
        }
        builder += `            </svg>
                                <div class="table-responsive border-0">
                                    <table class="unpadded-table border-0">
                                        <tr class="bg-body border-0">
                                            <th class="half-width bg-body border-0 pt-0" style="font-size: 0.85rem;">${numBars} days ago</th>
                                            <th class="half-width bg-body border-0 pt-0 text-end" style="font-size: 0.85rem;">now</th>
                                        </tr>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>`;
        ++sp;
    }
    builder += "</div>";
    document.getElementById("services-gen").innerHTML = builder;
    document.getElementById(`collapse${ll-1}`).addEventListener("show.bs.collapse", event => {
        document.getElementById(`accordbt-${ll-1}`).classList.replace("rounded-bottom-4", "rounded-bottom-0");
    });
    document.getElementById(`collapse${ll-1}`).addEventListener("hide.bs.collapse", event => {
        document.getElementById(`accordbt-${ll-1}`).classList.replace("rounded-bottom-0", "rounded-bottom-4");
    });
    // since the accordion is always redone after the table, this is a safe operation
    // if that changes, both need to have it
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    // @ts-ignore
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

function getDisplayCategory(): number {
    const w = window.innerWidth;
    if (w < PCT_BREAKDOWN_SPLIT)
        return 0;
    if (w < SINGLE_MONTH_SHIFT)
        return 1;
    if (w < EXPANSION_SIZE)
        return 2;
    if (w < PCT_BREAKDOWN_SPLIT_TWO)
        return 3;
    if (w < DOUBLE_MONTH_SHIFT)
        return 4;
    return 5;
}

// We only need to actually change anything if the viewport changes
function detectViewportChange(): void {
    let new_check: number = getDisplayCategory();
    if (serverListExpanded != new_check) {
        serverListExpanded = new_check;
        generate_table();
        generate_accordion();
    }
}

window.onresize = detectViewportChange;

// We could just refresh the page, which would reload everything.
// However, it's much more efficient to just re-request the API data
function refreshOnInterval(): void {
    // This is perfectly valid code, but ts doesn't like the type issues
    // Thus, we must:
    // @ts-ignore
    serverListInitialization();
}

setInterval(refreshOnInterval, 60000);