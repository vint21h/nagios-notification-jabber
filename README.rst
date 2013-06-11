.. nagios-notification-jabber
.. README.rst

A nagios-notification-jabber documentation
==========================================

    *nagios-notification-jabber is a Nagios-plugin that send Nagios notifications via jabber*

.. contents::

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vint21h/nagios-notification-jabber.git``. Or download latest release from https://github.com/vint21h/nagios-notification-jabber/tags.
* Run ``python ./setup.py install`` from repository source tree or unpacked archive under root user. Or use pip: ``pip install nagios-notification-jabber``.

Configuration
-------------
* Read and understand Nagios documentation.
* Create Nagios commands definitions like this:

::

    # 'host-notify-by-jabber' command
    define command
    {
        command_name    host-notify-by-jabber
        command_line    /usr/bin/notification_jabber.py -r $CONTACTPAGER$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$"
    }

    # 'service-notify-by-jabber' command
    define command
    {
        command_name    service-notify-by-jabber
        command_line    /usr/bin/notification_jabber.py -r $CONTACTPAGER$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$"
    }

* Add to your contact definition option ``pager`` with your Jabber ID value and add to ``service_notification_commands`` and ``host_notification_commands`` contact definition options ``service-notify-by-jabber`` and ``host-notify-by-jabber`` values respectively.

* Copy ``/usr/share/doc/nagios-notification-jabber/notification_jabber.ini`` to ``/etc/nagios`` with your nagios bot credentials and optionaly resource by Nagios instance hostname or custom string. Attention: nagios user must have ``notification_jabber.ini`` read permissions.

Licensing
---------
nagios-notification-jabber is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
For complete license text see COPYING file.


Contacts
--------
**Project Website**: https://github.com/vint21h/nagios-notification-jabber

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
