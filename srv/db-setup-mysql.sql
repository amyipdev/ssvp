create database ssvp;
grant all privileges on ssvp.* to 'ssvp'@'%' identified by 'ssvp-demo';
use ssvp;
create table ssvp_day_logs (
    logDate date not null,
    serverName text not null,
    serverStatus integer not null
);
create table ssvp_interval_logs (
    logDate datetime not null,
    serverName text not null,
    serverStatus boolean not null
);
create table ssvp_cached_stats (
    monthlyUptime double not null,
    yearlyUptime double not null,
    allTimeUptime double not null,
    serverName text not null,
    currentStatus integer not null
);
create table ssvp_events (
    eventID integer not null,
    serverName text not null,
    eventName text not null,
    eventDescription text,
    startTime datetime not null,
    endTime datetime,
    severity integer
);