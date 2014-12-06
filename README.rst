BrowseGit
=========

BrowseGit is a SublimeText plugin. It solves a problem of sharing the links
to the source code pushed to bitbucket.org or github.com.

Plugin defines ``browse_git`` command, which generates the URL to the page
on a GIT hosting for the current position in the file and opens it in a browser.

Tested with Sublime Text 3 in OS X, should work in Linux too.

Installation
------------

Clone plugin source code into `Packages directory <https://www.sublimetext.com/docs/3/packages.html>`_ and add a keymap for ``browse_git`` command to `User Key Bindings <http://www.sublimetext.com/docs/3/settings.html>`_ in OS X::

    { "keys": ["super+option+g"], "command": "browse_git" }

and in Linux::

    { "keys": ["control+alt+g"], "command": "browse_git" }


License
-------

* Free software: MIT
