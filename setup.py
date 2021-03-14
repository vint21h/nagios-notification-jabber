#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nagios-notification-jabber
# setup.py


from setuptools import setup, find_packages


# metadata
VERSION = (1, 0, 3)
__version__ = ".".join(map(str, VERSION))

DATA = [
    "README.rst",
    "COPYING",
    "AUTHORS",
    "notification_jabber.ini",
]

setup(
    name="nagios-notification-jabber",
    version=__version__,
    packages=find_packages(exclude=["tests.*", "tests"]),
    scripts=[
        "notification_jabber.py",
    ],
    install_requires=[
        "slixmpp>=1.7.0",
    ],
    package_data={
        "nagios-notification-jabber": DATA,
    },
    data_files=[
        ("share/doc/nagios-notification-jabber/", DATA),
    ],
    author="Alexei Andrushievich",
    author_email="vint21h@vint21h.pp.ua",
    description="Notifications via jabber Nagios plugin",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license="GPLv3+",
    license_file="COPYING",
    url="https://github.com/vint21h/nagios-notification-jabber",
    download_url="https://github.com/vint21h/nagios-notification-jabber/archive/{version}.tar.gz".format(  # noqa: E501
        version=__version__
    ),
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    test_suite="tests",
    keywords=[
        "nagios",
        "jabber",
        "notification-jabber",
        "plugin",
        "notification-jabber-plugin",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Plugins",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    extras_require={
        "test": [
            "attrs==20.3.0",
            "bandit==1.7.0",
            "black==20.8b1",
            "check-manifest==0.46",
            "check-wheel-contents==0.2.0",
            "contextlib2==0.6.0.post1",
            "coverage==5.5",
            "coveralls==3.0.1",
            "darglint==1.7.0",
            "dodgy==0.2.1",
            "dotenv-linter==0.2.0",
            "flake8-annotations-complexity==0.0.6",
            "flake8-annotations-coverage==0.0.5",
            "flake8-bugbear==21.3.2",
            "flake8-docstrings==1.5.0",
            "flake8-fixme==1.1.1",
            "flake8==3.8.4",
            "interrogate==1.3.2",
            "isort==5.7.0",
            "mypy==0.812",
            "pep8-naming==0.11.1",
            "pre-commit-hooks==3.4.0",
            "pre-commit==2.11.1",
            "pygments==2.8.1",
            "pylint==2.7.2",
            "pyroma==3.1",
            "pytest-cov==2.11.1",
            "pytest-mock==3.5.1",
            "pytest-tldr==0.2.4",
            "pytest==6.2.2",
            "readme_renderer==29.0",
            "removestar==1.2.2",
            "seed-isort-config==2.2.0",
            "tabulate==0.8.9",
            "tox-gh-actions==2.4.0",
            "tox-pyenv==1.1.0",
            "tox==3.23.0",
            "twine==3.3.0",
            "yesqa==1.2.2",
        ]
    },
)
