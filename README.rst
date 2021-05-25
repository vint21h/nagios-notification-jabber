.. nagios-notification-jabber
.. README.rst

A nagios-notification-jabber documentation
==========================================

|GitHub|_ |Coveralls|_ |pypi-license|_ |pypi-version|_ |pypi-python-version|_ |pypi-format|_ |pypi-wheel|_ |pypi-status|_

    *nagios-notification-jabber is a Nagios-plugin that send Nagios notifications via jabber*

.. contents::

Installation
------------
* Obtain your copy of source code from the git repository: ``$ git clone https://github.com/vint21h/nagios-notification-jabber.git``. Or download the latest release from https://github.com/vint21h/nagios-notification-jabber/tags/.
* Run ``$ python ./setup.py install`` from the repository source tree or unpacked archive. Or use pip: ``$ pip install nagios-notification-jabber``.

Configuration
-------------
* Read and understand Nagios documentation.
* Create Nagios commands definitions like this:

::

    # "host-notify-by-jabber" command
    define command
    {
        command_name    host-notify-by-jabber
        command_line    /usr/bin/notification_jabber.py -r $CONTACTPAGER$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$"
    }

    # "service-notify-by-jabber" command
    define command
    {
        command_name    service-notify-by-jabber
        command_line    /usr/bin/notification_jabber.py -r $CONTACTPAGER$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$"
    }

* Add to your contact definition option ``pager`` with your Jabber ID value and add to ``service_notification_commands`` and ``host_notification_commands`` contact definition options ``service-notify-by-jabber`` and ``host-notify-by-jabber`` values respectively.

* Copy ``/usr/share/doc/nagios-notification-jabber/notification_jabber.ini`` to ``/etc/nagios`` with your nagios bot credentials. Attention: nagios user must have ``notification_jabber.ini`` read permissions.

nagios-notification-jabber is able to send message to MUC rooms without any additional configuration, just specify MUC room ID as a notification recipient.
Also yu can specify notification resource just by adding it to JID in the config file: ``jid = nagios@example.com/bot``

Licensing
---------
nagios-notification-jabber is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.

Contacts
--------
**Project Website**: https://github.com/vint21h/nagios-notification-jabber/

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>

For other authors list see AUTHORS file.


.. |GitHub| image:: https://github.com/vint21h/nagios-notification-jabber/workflows/build/badge.svg
    :alt: GitHub
.. |Coveralls| image:: https://coveralls.io/repos/github/vint21h/nagios-notification-jabber/badge.svg?branch=master
    :alt: Coveralls
.. |pypi-license| image:: https://img.shields.io/pypi/l/nagios-notification-jabber
    :alt: License
.. |pypi-version| image:: https://img.shields.io/pypi/v/nagios-notification-jabber
    :alt: Version
.. |pypi-python-version| image:: https://img.shields.io/pypi/pyversions/nagios-notification-jabber
    :alt: Supported Python version
.. |pypi-format| image:: https://img.shields.io/pypi/format/nagios-notification-jabber
    :alt: Package format
.. |pypi-wheel| image:: https://img.shields.io/pypi/wheel/nagios-notification-jabber
    :alt: Python wheel support
.. |pypi-status| image:: https://img.shields.io/pypi/status/nagios-notification-jabber
    :alt: Package status
.. _GitHub: https://github.com/vint21h/nagios-notification-jabber/actions/
.. _Coveralls: https://coveralls.io/github/vint21h/nagios-notification-jabber?branch=master
.. _pypi-license: https://pypi.org/project/nagios-notification-jabber/
.. _pypi-version: https://pypi.org/project/nagios-notification-jabber/
.. _pypi-python-version: https://pypi.org/project/nagios-notification-jabber/
.. _pypi-format: https://pypi.org/project/nagios-notification-jabber/
.. _pypi-wheel: https://pypi.org/project/nagios-notification-jabber/
.. _pypi-status: https://pypi.org/project/nagios-notification-jabber/
