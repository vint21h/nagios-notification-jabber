#!/usr/bin/env python
# -*- coding: utf-8 -*-

# notification_jabber
# setup.py

import os
import warnings
from setuptools import setup, find_packages

from notification_jabber import (
	__author__,
	__email__,
    __version__,
    __licence__,
    __description__,
    __url__,
)

SHARE_FILES = ['README.rst', 'notification_jabber.ini', 'COPYING', ]

setup(
    name = "notification_jabber",
    version = __version__,
    packages = find_packages(),
    scripts = ['notification_jabber.py', ],
    install_requires = ['docutils', 'xmpppy', ],
    package_data = {
    	'': SHARE_FILES,
    },
    data_files = [
			('/usr/share/doc/notification_jabber/', SHARE_FILES),
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
