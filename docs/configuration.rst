Configuration
=============

SSVP is very versatile, and designed to run in a wide variety of environments.

Configuration file
------------------

The SSVP configuration file must be stored at :code:`srv/ssvp-config.json`. A new one can be created by:

- Manually entering the options seen below
- Running :code:`python3 installer/gen_config.py`
- Copying and editing :code:`srv/ssvp-config.json.example`

The file options are:

- :code:`enable_host_ipv6`: Determines whether to enable IPv6 support. On non-Linux OSes, having this option enabled may disable IPv4 support. (optional)
    - Allowed values: :code:`true`, :code:`false`
- :code:`ssl`: Determines SSL support, and configuration settings.
    - Allowed values:
        - :code:`null`: disables SSL
        - :code:`["/path/to/cert.pem", "/path/to/key.pem"]`: uses existing certificates/keyfiles
        - :code:`"adhoc"`: Uses self-signed/ad-hoc certificates
- :code:`port`: Port number for the SSVP server (optional)
    - Allowed values: any integer from 1 to 65535 (note: 1-1024 require root/sudo)
- :code:`instance_name`: Name put in the navbar brand for the instance
    - Allowed values: any string
- :code:`splash`: Splash text for the main page (optional)
    - Allowed values: any string
- :code:`servers`: List of servers, set as an object
    - Allowed values: must fit the following schema:
        .. code-block:: json
            
            "name_of_server": {
                "ip": "ip address (url for http)",
                "module": "testing module name",
                "args": "list of module arguments"
            }
            
    - The :code:`module` can be one of :code:`ping`, :code:`http`, :code:`tcp`, :code:`ssvplwc`

- :code:`services`: List of services, set as an object
    - Allowed values: must fit the servers schema
- :code:`database`: Database information
    - Note: the only options required on sqlite3 are :code:`host`, :code:`type`, and :code:`prefix`
    - :code:`type`: database type
        - Either :code:`mysql`, :code:`postgres`, :code:`sqlite3`
    - :code:`host`: database host IP/sqlite3 file path
        - Valid IPv4 or IPv6 address
    - :code:`port`: database port
        - Valid TCP port (unix sockets are not supported)
    - :code:`username`: database username
    - :code:`password`: database password
    - :code:`database`: name of database in the DB system
    - :code:`prefix`: prefix for tables
- :code:`contact`: user contact information (optional)
    - :code:`name`: user's name, display name, or organization name
    - :code:`mastodon`: mastodon profile (format: :code:`@username@home.server`)
    - :code:`github`: GitHub profile (just the username)
    - :code:`git`: link to custom git server
    - :code:`email`: email address
- :code:`docs`: set to :code:`"local"` to use local documentation instead of `GitHub Pages <https://ssvp.docs.amyip.net>_    

Systemd
-------

If you're using systemd, there's four main options:

- **Enabling**: setting a unit to run at boot (:code:`systemctl enable unit_name`)
- **Disabling**: removing a unit from the at-boot list (:code:`systemctl disable unit_name`)
- **Starting**: launching a unit for the current boot (:code:`systemctl start unit_name`)
- **Stopping**: stopping a unit for the current boot (:code:`systemctl stop unit_name`)

    It should be noted that, to start a unit at the same time as enabling it, you should pass the :code:`--now` flag, as in
    :code:`systemctl enable --now unit_name`

SSVP uses three main units for operation:

- :code:`ssvp-gunicorn.service`: Production web server
- :code:`ssvp-werkzeug.service`: Development web server
- :code:`ssvp-interval.timer`: Server uptime checking timer

Some important notes:

1. :code:`ssvp-gunicorn.service` and :code:`ssvp-werkzeug.service` should not be run at the same time; you only need one web server.
   If you try and run both at once, systemd will kill the first one.
2. For those with some experience in systemd, it is very important that :code:`ssvp-interval.timer` not have its suffix left off (running as :code:`systemctl start ssvp-interval`).
   Doing so will just run the server uptime checker just once, and not periodically.
3. Do not remove :code:`ssvp-interval.service`; it gets called by :code:`ssvp-interval.timer`.

So, for instance, to set up a standard configuration:

.. code-block:: bash

    systemctl enable --now ssvp-gunicorn.service
    systemctl enable --now ssvp-interval.timer
