# notification_jabber
# README.rst

A notification_jabber documentation
===================================

    *notification_jabber is a Nagios-plugin that send Nagios notifications via jabber*

Installation
------------
* Obtain your copy of source code from git repository: git clone https://vint21h@github.com/vint21h/notification_jabber.git
* Run setup.py install under root user.

Configuration
-------------
* Create Nagios commands definitions like this:

# 'host-notify-by-jabber' command definition
define command
{
    command_name    host-notify-by-jabber
    command_line    $USER1$/notification_jabber -r $CONTACTPAGER$ -m "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info: $HOSTOUTPUT$"
}

# 'notify-by-jabber' command definition
define command
{
    command_name    notify-by-jabber
    command_line    $USER1$/notification_jabber -r $CONTACTPAGER$ -m "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICEDESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$"
}

* Add to your contact definition option pager with your jabber id and add to service_notification_commands and host_notification_commands options notify-by-jabber and host-notify-by-jabber values respectively.

* Then edit your notification_jabber.ini.

Contacts
--------
**Project Website**: https://github.com/vint21h/notification_jabber

**Author**: Alexei Andrushievich <vint21h@vint21h.pp.ua>
