.. nagios-notification-jabber
.. README.rst

A nagios-notification-jabber documentation
===================================

    *nagios-notification-jabber is a Nagios-plugin that send Nagios notifications via jabber*

.. contents::

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://github.com/vint21h/nagios-notification-jabber.git``. Or download latest release from https://github.com/vint21h/nagios-notification-jabber/downloads.
* Run ``./setup.py install`` from repository source tree or unpacked archive under root user.

Configuration
-------------
* Read and understand Nagios documentation.
* Add Nagios variable ``$NJ$=/usr/bin/notification_jabber.py``
* Create Nagios commands definitions like this:

::

    # 'host-notify-by-jabber'
    define command
    {
        command_name    host-notify-by-jabber
        command_line    $NJ$ -r $CONTACTPAGER$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$"
    }

    # 'notify-by-jabber'
    define command
    {
        command_name    notify-by-jabber
        command_line    $NJ$ -r $CONTACTPAGER$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$"
    }

* Add to your contact definition option ``pager`` with your Jabber ID value and add to ``service_notification_commands`` and ``host_notification_commands`` contact definition options ``notify-by-jabber`` and ``host-notify-by-jabber`` values respectively.

* Populate ``/etc/notification_jabber.ini`` with your nagios bot credentials and optionaly resource by Nagios instance hostname or custom string.

Contacts
--------
**Project Website**: https://github.com/vint21h/nagios-notification-jabber

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
