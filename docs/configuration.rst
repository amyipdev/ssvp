Configuration
=============

Here's all of the configuration options:

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