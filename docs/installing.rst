Installation
============

Installation of SSVP is usually simple, thanks to the easy installer (:code:`./install.sh`).

Supported Operating Systems
---------------------------

Right now, we're currently focusing on just supporting Linux. \*BSD and macOS support may come in the future; Windows support is unlikely.

Theoretically, any Linux distribution should work. We currently only officially support **Debian 12** and **Fedora 38**.

Our dependency installer currently has support for most **apt**-based and **dnf/yum**-based distributions. Support for other package managers is a `planned feature <https://github.com/amyipdev/ssvp/issues/23>`_.
The dependency verifier works on all systems, **but cannot check the presence of libpq and its headers**.

If you have to install dependencies manually, be aware that you need all of the packages list `here <https://github.com/amyipdev/ssvp/blob/main/installer/autoinstall-deps-system.sh>`_.

Downloading SSVP
----------------

You need Git in order to download SSVP.

Once Git is installed, run:

.. code-block:: bash

    git clone --depth=1 https://github.com/amyipdev/ssvp

Running the Installation Script
-------------------------------

To run the installation script, from the SSVP download directory, run:

.. code-block:: bash

    ./install.sh
    
Installation Components
-----------------------

The installer will prompt you on whether to run several of its modules. Defaults are always in brackets, such as :code:`not default/[default]`.

The first option is to autoinstall system dependencies. You should only respond yes if you are on a **Fedora** or **Debian** derivative system. This includes:

- `Red Hat Enterprise Linux <https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux>`_
- `Fedora Linux <https://fedoraproject.org/>`_
- `Debian Linux <https://www.debian.org/>`_
- `Ubuntu Linux <https://ubuntu.com/>`_ (and its derivatives, such as `Kubuntu <https://kubuntu.org/>`_ and `Linux Mint <https://linuxmint.com/>`_)
- `CentOS Linux <https://centos.org/>`_, `Rocky Linux <https://rockylinux.org/>`_, and `Alma Linux <https://almalinux.org/>`_

If you decline the option, you'll be given the choice to verify your system dependencies. This just checks that they're all available in the PATH, and works on any system.

If you don't have a virtual environment already, you'll be asked if you want one created. This is highly recommended, and on many systems, it is extremely difficult not to use one.
If one exists or you opted to create one, you'll be asked if you want to source the venv. This is mandatory for it to work properly.

You'll then be asked about installing other types of dependencies. The PyPI option installs dependencies from :code:`requirements.txt`. If you have no intention of using or testing postgres,
you may be able to get away with not installing `psycopg2`; it takes a while to compile on lower-powered systems and takes up a decent amount of space, so skipping it may be of interest.
All of the node dependencies are required for building SSVP; as such, you should generally opt to autoinstall the NPM dependencies. The last option is site dependencies; this just runs
:code:`make` prior to setting everything else up. If you're planning on running `make` for some purpose later anyways, this is unnecessary.

You'll then be asked to work with the database and with the SSVP configuration. You can always configure things later, but the config file script greatly helps with initial setup.
The database step presumes you have an existing database, or that you're going to be using `sqlite3`. You'll need database credentials on hand when running the initialization.
If you use the defaults for databases, you should use the defaults in the config file database section. Initializing cached statistics is also highly recommended, as SSVP will
fail to run without the entries.

The full installation is meant for server installs, when you want to segregate the installations and have automation set up for you automatically. If you're a developer,
this often is not necessary. Cron is one option for installation; systemd is another. Read the `configuration guide <configuration.html>`_ for more information on setting up systemd.
The "enable on boot" option for systemd will take care of everything. OpenRC is not currently supported, but may be added in the future; the same goes for other systems (sysvinit, upstart, runit, shepherd).

You're now done with the installation. You can run the server by running `srv/tmux.sh`. It should print :code:`no current client` when done. You can check on the server by running `tmux attach`,
and disconnect from it by pressing `CTRL-b d`.

If you need to change settings in your configuration file, please see the `configuration guide <configuration.html>`_.