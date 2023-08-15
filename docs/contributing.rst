Contributing
============

Thanks for wanting to help with the development of SSVP! Here's how you can contribute.

Ways to Contribute
------------------

- **Submit bug reports**: when you find a problem in SSVP, report it `here <https://github.com/amyipdev/ssvp/issues>`_.
- **Write code**: See below on how to write code and submit it to SSVP.
- **Contribute to documentation**: Similar procedures to writing code, but work is done in the :code:`docs/` folder.
- **Translation**: We don't have internationalization set up yet, but if you'd like to assist, `let us know <mailto:amy@amyip.net>`_.

Getting Started
---------------

The first thing you need to do is to create a fork of the project. You need a GitHub account for this; if you don't want to make one, reach out to us.

To create a fork, go to the `SSVP project page <https://github.com/amyipdev/ssvp>`_, and click the Fork button:

.. image:: _images/fork.png

You then need to download your fork to your local machine (make sure you have git installed):

.. code-block:: bash

    git clone --depth=1 https://github.com/yourGitHubUsername/ssvp
    
You then want to run the `installation process <installing.html>`_. This will help you get all your dependencies installed.
If you're just doing development work, you probably won't have a database already set up yet. As a result, we recommend using a local `sqlite3` installation
when setting up the database functionality. When choosing an installation directory, keep it as the default option. Don't set an "autorunner" or "server reboot launch method".

Creating a Patch
----------------

Now that you're all set up, it's time to create a patch.

First, you need to establish a branch for your patch. It should be given a relevant name; for instance, if you're implementing Windows support for the interval module, a possible branch name could be `interval-windows-support`.

Once you've chosen the name, create and switch to the branch:

.. code-block:: bash

    git checkout -b your-branch-name
    
You can now freely modify files, building your patch.

If the patch affects real code, we recommend that you run a linter on what you changed.
You can find out more information about linting in the `maintenance guide <maintaining.html>`_.

When you're ready to save an interval of your progress, run:

.. code-block:: bash

    git add -A
    git commit
    
Saving an interval doesn't automatically push all the changes. All of the "commits" will be sent when you propose the changes.

Running the commit command opens up a dialog asking you to put a message for the commit. This should be of the form:

.. code-block::

    active subject line
    
    This patch (say what the patch does). (Justify why it should be added).
    
    Signed-off-by: Your Name <email@address.tld>
    
The subject line should be stated as an action; instead of "changes x to y", it should be "change x to y".

If your commit is resolving a bug, add another line, where XX is the issue number:

.. code-block::

    Fixes: #XX
    
There's also other important tags to add on; `we use the Linux kernel project's system for useful tags <https://www.kernel.org/doc/html/latest/process/submitting-patches.html>`_.

When you're done creating commits, run the following command:

.. code-block::

    git push --set-upstream origin (name of your branch)
    
Then, go to your fork on GitHub. As long as you do this step shortly after you push, it should say something about your branch having "recent changes". Click the button to submit a pull request.
If there is no button there, go to pull requests, and open one manually.

The source branch should be set as your new branch. The target branch should be set as amyipdev/main. You can then write a title and description for your PR. It should
follow the same format as the commit message format, with the subject line becoming the title.

When you're ready, you can click the "create pull request" button. This will send it off.

Reviewing
---------

Someone will come along to review your patch. They may have suggestions and/or comments on it; these should be addressed when you are able.
You may need to add additional comments to fix issues presented by reviewers.

When ready, the PR will be accepted. That means your code has made it into SSVP.

Resetting Your Fork
-------------------

When you make your next patch, before branching, you should sync your fork. This can be done with the "Sync" button on GitHub when you're viewing your main branch.