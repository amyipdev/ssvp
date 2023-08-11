Installation
============

Installation of SSVP is usually simple, thanks to the
easy installer (:code:`./install.sh`).

Supported Operating Systems
---------------------------

Support has a few main levels:

- Level 0: **Great Support**. Every commit is thoroughly tested on these
  levels, usually due to developers running this on their own machines.
  Support on these should be perfect. It is not necessary for a platform
  to be level 0 for SSVP to be production-ready on it; however, level 0
  platforms are the least likely to have bugs.
- Level 1: **Good Support**. These are environments known to work well.
  No workarounds should be required. These platforms should survive major
  changes to SSVP with ease, are tested in pipelines, and will always be
  tested before any `"minor" <https://semver.org/>`_ releases.
  They should be perfectly fine for production.
- Level 2: **Decent Support**. These environments should work just fine.
  Minimal to no workarounds should be required. It is recommended to run
  a release version of SSVP on these platforms, instead of running main.
  Minor releases will have changes tested; however, testing may not be
  as thorough. These are still fine to use in production, but a level 1
  platform is recommended.
- Level 3: **Theoretical Support**. In theory, this platform should work
  fine; it might have even been tested once. However, it's unknown whether
  it works for sure. These platforms may require workarounds, and are not
  recommended.
- Level 4: **Unknown Support**. These platforms have completely unknown
  support. They have never been tested. Workarounds will likely be required.
- Level -1: **Borked**. These platforms are known not to work. If you'd like
  to help make them work, feel free to `contribute <contributing.html>`_.

..
  TODO: alphabetize

.. list-table::

  * - Operating System
    - Support Level
    - Required OS Version
    - Packaging Info
  * - Fedora
    - 0
    - unknown
    -
  * - Debian
    - 0
    - unknown
    -
  * - NixOS
    - 1
    - 23.11/unstable
    -
  * - Ubuntu
    - 3
    - unknown
    -

If you have to install dependencies manually, be aware that you need all of the packages list `here <https://github.com/amyipdev/ssvp/blob/main/installer/autoinstall-deps-system.sh>`_.

If you're on **NixOS**, jump to the :ref:`NixOS instructions<NixOS>`.

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

NixOS
-----

.. _NixOS:

This section is only necessary for those using NixOS.

Because the Nix installer can't create a configuration file of its own, you need to create one.
See `the configuration manual <configuration.html>`_ for how to do this.

First, you need to open up your configuration file (either a local one, or `/etc/nixos/configuration.nix`). Locate the :code:`let` list, and add:

.. code-block:: nix

    ssvp = builtins.fetchTarball "https://github.com/amyipdev/ssvp/archive/nix-shell-distrib.tar.gz";

Then, locate the :code:`imports` list, and add:

.. code-block:: nix

    "${ssvp}/service.nix"

Below the end of the imports list, then add:

.. code-block:: nix

    services.ssvp = {
        enable = true;
        configFile = "/path/to/ssvp-config-file";
    }

Save and exit the file. Then, reload your nix config:

.. code-block:: bash

    nixos-reload switch

SSVP is now up and running.    