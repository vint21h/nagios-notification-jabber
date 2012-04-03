.. notification_jabber
.. README.rst

A notification_jabber documentation
===================================

    *notification_jabber is a Nagios-plugin that send Nagios notifications via jabber*

Installation
------------
* Obtain your copy of source code from git repository: ``git clone https://vint21h@github.com/vint21h/notification_jabber.git``
* Run setup.py install under root user.

Configuration
-------------
* Read and understand Nagios documentation.
* Add Nagios variable $NJ$=/usr/bin/notification_jabber
* Create Nagios commands definitions like this:

# 'host-notify-by-jabber' command definition
define command
{
    command_name    host-notify-by-jabber
    command_line    $NJ$ -r $CONTACTPAGER$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$"
}

# 'notify-by-jabber' command definition
define command
{
    command_name    notify-by-jabber
    command_line    $NJ$ -r $CONTACTPAGER$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$"
}

* Add to your contact definition option pager with your jabber id and add to service_notification_commands and host_notification_commands options notify-by-jabber and host-notify-by-jabber values respectively.

* Copy notification_jabber.ini from /usr/share/doc/notification_jabber to /etc. Populate notification_jabber.ini with your nagios bot credentials and optionaly resource by Nagios instance hostname or custom string.

Contacts
--------
**Project Website**: https://github.com/vint21h/notification_jabber

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
