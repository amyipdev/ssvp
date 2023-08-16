Maintenance
===========

To keep SSVP clean, we have several standards for how the project should be maintained.

Pull Requests
-------------

PRs should be continually commented on until they are eventually rejected or merged.

Merge Types
~~~~~~~~~~~

Under no circumstances, except when absolutely required (major conflics), should merge commits be used.
In most cases, a resolution commit and a squash can serve the purpose of a merge commit.

Generally, commits should be applied with a rebase. Rebasing isn't perfect, but it does perform a lot
better for most purposes than merge commits, and keeps authorship.

If there are a *lot* of commits, then a squash commit may be necessary. This is more acceptable
with single ownership of the commits; however, it is more preferred for users to pre-squash.
Whenever a squash commit is required, it's important to add Co-developed-by for every author.

Tagging
-------

Tagging a release is a great occasion, but there's several things to keep in mind:

- Anything with the version number needs to be updated. This should be done in a single commit
  (this is a great time for a squash commit if necessary). It should be the last commit before
  tagging.
- Testing releases:
  - Level 0 releases must be deeply, deeply tested.
  - Level 1 releases should be thoroughly tested.
  - Level 2 releases should have basic testing done.
- Running: a live instance demonstrating the new version must exist; this will usually be status.amyip.net.
- Ensure that everything's been linted, reformatted, etc.
- Verify documentation is up-to-date - both in terms of instructions, and in terms of Sphinx's version number
  (this is something that's not always covered)
  
Packaging
---------

When packaging, local changes to :code:`release-info.json` should be made, removing the :code:`+` and adding any appropriate suffixes.

For instance, for in-progress :code:`v0.3.0`, the release version is set as :code:`0.3.0+`. When packaging, this should be changed
to :code:`0.3.0`. The commit after the tag would then change the release version to :code:`0.4.0+`.

RPMs
~~~~

Building should only be done on a **clean system**. Make sure you don't have an SSVP config file, or anything else;
you risk leaking secrets.

First, make sure you have the necessary dependencies installed:

.. code-block:: bash

  dnf install -y make jq nodejs nodejs-npm rpmdevtools rpmlint

Then, just run:

.. code-block:: bash

  make rpm

The RPM will be generated at :code:`rpmbuild/RPMS`.

Enterprise Linux RPMs
<<<<<<<<<<<<<<<<<<<<<

.. _ELRPMs:

There is a `known issue <https://github.com/amyipdev/ssvp/issues/49>`_ when building RPMs or using
:code:`install.sh` on Enterprise Linux distributions (**Rocky**, **RHEL**, **Alma**, **CentOS**, **Oracle**).

Detection
>>>>>>>>>

You can tell if your distribution is Enterprise Linux by running the following command on a known-installed
package (:code:`bash` used as an example):

.. code-block:: bash

  dnf list bash

and then looking at the last component of the second column. If the system is Enterprise Linux, it will
be of the format :code:`elN`, where N is some number. If it does not contain :code:`el`, then it is not
Enterprise Linux, and this is not the bug source.

Fixing
>>>>>>

The fix depends on whether you are using :code:`install.sh` or using the RPM; if the former, apply the
following edits to :code:`srv/autoinstall-deps-system.sh`, if the latter, to :code:`ssvp.spec.fmt`.

- :code:`nodejs-npm` changed to :code:`npm`

You also need to install :code:`python3-pip`, and then run:

.. code-block:: bash

  pip3 install pyopenssl gunicorn Flask mysql-connector-python

If you are building an RPM, you must remove those packages from :code:`ssvp.spec.fmt`.

SUSE
<<<<

.. _SUSE:

The development package installation list is slightly different:

.. code-block:: bash

  zypper install make nodejs npm rpm-build rpmdevtools rpmlint jq

You can then build and install the RPM as normal. Two things will come up:

1. You'll be asked about python3-flask. You should just choose to ignore
   the issue. You then later need to run:

   .. code-block:: bash

      zypper install python3-pip
      pip3 install Flask

2. After that, it'll throw up a warning about the RPM being unsigned. This
   is fully safe to ignore.

Linting
-------

It is good to lint whenever you're going to commit; however, it is understood that this can be tedious.
As such, contributors are given discretion on whether to lint. Most small issues will be caught when
preparing for release, so lint checking is not critical; further, because of the many linting things
that can come up that are unimportant to SSVP, we do not run linters in CI. It is absolutely imperative
to lint, however, when preparing for a release.

Linting depends on the language, and should be run on every modified file (and, for releases, every file).

Python
~~~~~~

First, ensure that :code:`pylint` is installed:

.. code-block:: bash

  pip3 install pylint

Then, for every file you need to lint, run:

.. code-block:: bash

  pylint <filename>

All warnings should be treated as **optional**; however, we have advice on the following warnings:

- **C0303/trailing-whitespace**: if your editor can fix this, it's welcome, but it's not critical.
  This commonly occurs in GPL notices.
- **C0301/line-too-long**: please separate into lines if reasonable If not, however, that is completely
  fine - sometimes code readability suffers when trying to comply.
- **Docstring objections**: C0114 and C0116 can be safely ignored. We do not use docstrings.
- **R1732/W1514**: tread carefully. Passage into reasonably-handled functions, such as :code:`json`
  functions, is acceptable (usage of directly passed open). However, if the file pointer is being
  used directly, then with should be used. Unspecified encodings are generally fine, with few
  exceptions; these exceptions cause bugs and would appear elsewhere, so relying on the linter
  is unnecessary.
- **C0123/unidiomatic-typecheck**: these can be optionally modified, but it is not necessary.
  Using type is perfectly fine, and isinstance should only be used if the switch is trivial.
- **C0411** and other import objections: these should be fixed within another commit, but are
  not critical; don't bother fixing them in their own commit.

Rust
~~~~

First, format the code:

.. code-block:: bash

  cargo fmt

Then, use `Rust Analyzer <https://rust-analyzer.github.io/>`_ to lint the code. This can often
be done directly in your IDE.

TypeScript
~~~~~~~~~~

Just run:

.. code-block:: bash

  eslint js/*

