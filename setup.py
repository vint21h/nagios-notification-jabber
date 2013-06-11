#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-jabber
# setup.py

from setuptools import setup, find_packages

VERSION = (0, 6, 7)
__version__ = '.'.join(map(str, VERSION))

DATA = ['README.rst', 'COPYING', 'notification_jabber.ini', ]

setup(
    name="nagios-notification-jabber",
    version=__version__,
    packages=find_packages(),
    scripts=['notification_jabber.py', ],
    install_requires=['xmpppy', ],
    package_data={
        'nagios-notification-jabber': DATA,
    },
    data_files=[
        ('share/doc/nagios-notification-jabber/', DATA),
    ],
    author="Alexei Andrushievich",
    author_email="vint21h@vint21h.pp.ua",
    description="Notifications via jabber Nagios plugin",
    long_description=open('README.rst').read(),
    license="GPLv3 or later",
    url="https://github.com/vint21h/nagios-notification-jabber",
    download_url="https://github.com/vint21h/nagios-notification-jabber/archive/%s.tar.gz" % __version__,
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ]
)
