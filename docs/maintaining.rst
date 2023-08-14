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

RPMs
~~~~

Building should only be done on a **clean system**. Make sure you don't have an SSVP config file, or anything else;
you risk leaking secrets.

First, make sure you have the necessary dependencies installed:

.. code-block:: bash

  dnf install -y rpmdevtools rpmlint

Then, just run:

.. code-block:: bash

  make rpm

The RPM will be generated at :code:`rpmbuild/RPMS`.