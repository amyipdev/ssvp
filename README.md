# ssvp: server statistics viewer project

This project is in a very early development stage. It is usable,
and you can view an example invocation [for my homelab](https://status.amyip.net),
but it is nowhere near production-ready yet.

There is not currently an organized installer. If you want to try
it out, make sure you have the following dependencies installed for
your system (package names dependent on distribution):

- sass
- python3 with pip and venv
- nodejs and npm

You also must have:

- A working MySQL or MariaDB server

And, we recommend (while SSVP is still in development):

- tmux

Step 1: Copy srv/ssvp-config.json.example to srv/ssvp-config.json

Step 2: Configure that file with your relevant information
(the only currently supported test module is ping)

Step 3: Make a venv (`python3 -m venv venv`), activate it
(`source venv/bin/activate`), and install
Python dependencies (`pip3 install -r requirements.txt`)

Step 4: Set up a cron job to run srv/interval.py
(recommended is 5 minutes, but any interval works)

Step 5: Install node dependencies (`npm i`)

Step 6: Compile sass and typescript (`make`)

Step 7: Launch the web server (`flask --app srv/app.py --host :: --port 80`)

> You may want to do this in tmux.

Please note that only Linux is fully supported. Other OSes may
not work or may require special workarounds, such as having to use
a single network stack (IPv4-only or IPv6-only) or requiring
interval.py to be run with superuser/administrator permissions.

Currently, support is highest-level for Debian 12 and Fedora 38.

HTTPS will be available in the future. Until then, you can run
it through a reverse proxy like nginx.