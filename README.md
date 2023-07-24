<div align="center">
<h1>ssvp: the server statistics viewer project</h1>
</div>
<div align="center">

![GitHub](https://img.shields.io/github/license/amyipdev/ssvp) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/amyipdev/ssvp)

</div>

SSVP is a lean, efficient status dashboard and uptime tracker for servers and services. It provides:
- A clean, easy-to-understand interface for your users to understand uptime metrics.
- A lightweight data collection platform supporting your existing back-end stack.
- An easy-to-interact-with API for more advanced data analysis.
- Support for tracking through a wide variety of methods, getting around any hurdles your stack creates.
- (WIP) Alerts for developers and users to stay on top of your platform.

You can view a live version run by the project owner at https://status.amyip.net.

The main thing that differs SSVP from other status pages is that it's designed for users first. It's AGPLv3-licensed and will always be free-as-in-freedom software, unlike many alternatives. It's also designed to be run externally, open to users; you don't have to expose any data you don't have to, which can help prevent side-channeling attacks.

## Installation

> These installation instructions will be better developed in the future. For now, they are meant for advanced users only.

A more streamlined way to install SSVP is currently in development. Until then, you can:
1. Install the npm and Python dependencies (in a venv).
2. Copy `srv/ssvp-config.json.example` to `srv/ssvp-config.json`, and configure it.
3. Run `make` to compile the Sass and Typescript.
4. Add a runner for `srv/interval.py` to run on intervals (ideally every 1-5 minutes) in your crontab.
5. Launch `srv/app.py` in a persistent environment (such as tmux).

## Contributing

There are two main ways you can help contribute to SSVP:
1. Use SSVP, and report any bugs you find in Issues.
2. Fix bugs and implement new features via PRs.

More detailed contribution instructions will be available at a later time.

## Limitations and Future Features

A list of planned features is available [here](https://github.com/amyipdev/ssvp/issues/1); if there's something you want included that isn't yet available, feel free to develop it and submit a PR!

## Licensing

This project was made by Amy Parker/amyipdev.

Copyright 2023 Amy Parker, amy@amyip.net.

SSVP is licensed under the AGPLv3. You can view the license in the LICENSE file.

## Inspiration

The project draws heavy inspiration from the design and setup of https://discordstatus.com, which runs on [Atlassian Statuspage](https://www.atlassian.com/software/statuspage).

It also draws inspiration from [Uptime Kuma](https://github.com/louislam/uptime-kuma). Uptime Kuma is great as an internal status page, and I would highly recommend it if the main intention of your status page is to be used internally instead of externally.

I wanted to work on a project which would give me a chance to do some web design, something I generally hate, and learn frameworks like Bootstrap and TypeScript.

