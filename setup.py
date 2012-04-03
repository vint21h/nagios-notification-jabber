#!/usr/bin/env python
# -*- coding: utf-8 -*-

# notification_jabber
# setup.py

import os
import warnings
from setuptools import setup, find_packages

from notification_jabber import __version__

setup(
    name = "notification_jabber",
    version = __version__,
    packages = find_packages(),
    scripts = ['notification_jabber.py'],
    install_requires = ['docutils', 'xmpppy', ],
    package_data = {
    	'': ['*.rst', '*.ini', 'COPYING', ],
    },
    author = "Alexei Andrushievich",
    author_email = "vint21h@vint21h.pp.ua",
    description = "Nagios-plugin that send Nagios notifications via jabber",
     long_description = open('README.rst').read(),
    license = "GPLv2 or later",
    url = "https://github.com/vint21h/notification_jabber",
    zip_safe = False,
    include_package_data = True,
)
