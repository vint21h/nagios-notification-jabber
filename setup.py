#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-jabber
# setup.py

from setuptools import setup, find_packages

from nnj import (
    __author__,
    __email__,
    __version__,
    __licence__,
    __description__,
    __url__,
)

SHARED_FILES = ['README.rst', 'COPYING', ]
CONFIG_FILES = ['nnj.ini', ]

setup(
    name = "nagios-notification-jabber",
    version = __version__,
    packages = find_packages(),
    scripts = ['nnj.py', ],
    install_requires = ['docutils', 'xmpppy', ],
    package_data = {
        '': (SHARED_FILES, CONFIG_FILES),
    },
    data_files = [
            ('/usr/share/doc/nagios-notification-jabber/', SHARED_FILES),
            ('/etc/', CONFIG_FILES),
    ],
    author = __author__,
    author_email = __email__,
    description = __description__,
    long_description = __description__,
    license = __licence__,
    url = __url__,
    zip_safe = False,
    include_package_data = True,
)
