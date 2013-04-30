#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-jabber
# setup.py

from setuptools import setup, find_packages

from notification_jabber import __author__, __email__, __version__, __licence__, __description__, __url__

SHARED_FILES = ['README.rst', 'COPYING', ]
CONFIG_FILES = ['notification_jabber.ini', ]

setup(
    name="nagios_notification_jabber",
    version=__version__,
    packages=find_packages(),
    scripts=['notification_jabber.py', ],
    install_requires=['xmpppy', ],
    package_data={
        '': (SHARED_FILES, CONFIG_FILES),
    },
    data_files=[
        ('/usr/share/doc/nagios-notification-jabber/', SHARED_FILES),
        ('/etc/nagios/', CONFIG_FILES),
    ],
    author=__author__,
    author_email=__email__,
    description=__description__,
    long_description=open('README.rst').read(),
    license=__licence__,
    url=__url__,
    zip_safe=False,
    include_package_data=True,
)
