wftools.py
==========

A collection of [Python](http://python.org) scripts used to boost front end
development of HTML5 applications.

Requeriments
------------

To run all the scripts properly you must install the [NPM](https://npmjs.org)
packages listed below and all [PyPI](http://pypi.python.org/pypi) packages
listed in `requeriments.txt` file:

        jade, less

How to use
----------

Create an empty directory and clone wftools.py
[repository](https://github.com/ademilsonfp/wftools.py) into it as `wft` (I
personally prefer to have only wftools.py clone and creating symbolic links as
need on each project directory).

Now you can run commands like:

        $ python wft jquery install
        $ python wft jade build

Custom builds
-------------

Feel free to write your custom build scripts based on wftools.py
[like this](https://gist.github.com/ademilsonfp/0c025e43ac4f2c78fec3).

Read the [source code](https://github.com/ademilsonfp/wftools.py) for more
detailed information of how to use or extend scripts.
