#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-jabber
# nnj.py

# Copyright (c) 2011-2012 Alexei Andrushievich <vint21h@vint21h.pp.ua>
# Notifications via jabber Nagios plugin [https://github.com/vint21h/nagios-notification-jabber]
#
# This file is part of nagios-notification-jabber.
#
# nagios-notification-jabber is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import sys

try:
    import os
    import ConfigParser
    from optparse import OptionParser
    import xmpp
except ImportError, err:
    sys.stderr.write("ERROR: Couldn't load module. %s\n" % err)
    sys.exit(-1)

# metadata
__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv3 or later"
__description__ = "Notifications via jabber Nagios plugin"
__url__ = "https://github.com/vint21h/nagios-notification-jabber"
VERSION = (0, 4, 0)
__version__ = '.'.join(map(str, VERSION))


def parse_cmd_line():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % (__version__)
    parser = OptionParser(version=version)
    parser.add_option("-r", "--recipient", action="store", dest="recipient",
                                        type="string", default="",
                                        metavar="RECIPIENT",
                                        help="message recipient Jabber ID")
    parser.add_option("-m", "--message", metavar="MESSAGE", action="store",
                                        type="string", dest="message",
                                        default="", help="message text")
    parser.add_option("-c", "--config", metavar="CONFIG", action="store",
                                        type="string", dest="config",
                                        help="path to config file")
    parser.add_option("-q", "--quiet", metavar="QUIET", action="store_false",
                                        default=False, dest="quiet",
                                        help="be quiet")

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    mandatories = ["recipient", "message", ]
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        sys.stdout.write("Mandatory command line option missing\n")
        sys.exit(0)

    return options


def check_config_file(ini):
    """
    Check config exist.
    """

    default_ini = "nnj.ini"
    if ini and os.path.exists(ini):  # user config file path
        return ini
    elif os.path.exists(default_ini):  # default config file path
        return default_ini
    elif os.path.exists(os.path.join("/etc", default_ini)):  # default config file path in /etc
        return os.path.join("/etc", default_ini)
    else:
        sys.stderr.write("ERROR: Config file %s don't exist\n" % ini)
        sys.exit(0)


def parse_config(configini):
    """
    Get connection settings from config file.
    """

    config = ConfigParser.ConfigParser()
    try:
        config.read(configini)
    except Exception:
        print "ERROR: Config file read %s error." % (configini)
        sys.exit(-1)
    configdata = {
                    'jid': config.get('JABBER', 'jid'),
                    'password': config.get('JABBER', 'password'),
                    'resource': config.get('JABBER', 'resource'),
    }

    # check mandatory config options supplied
    mandatories = ["jid", "password", ]
    if not all(configdata[mandatory] for mandatory in mandatories):
        sys.stdout.write("Mandatory command line option missing\n")
        exit(0)

    return configdata


def send_message(config, recipient, message):
    """
    Connect to server and send message.
    """

    jid = xmpp.JID(config['jid'])  # JID object
    client = xmpp.Client(jid.getDomain(), debug=[])
    try:
        client.connect()
        client.auth(jid.getNode(), config['password'], config['resource'])
        client.sendInitPresence()
    except Exception, err:
        sys.stdout.write("ERROR: Couldn't connect or auth on server. %s\n" % err)
        sys.exit(-1)
    xmessage = xmpp.Message(recipient, message)
    xmessage.setAttr('type', 'chat')
    try:
        client.send(xmessage)
    except Exception, err:
        sys.stdout.write("ERROR: Couldn't send message. %s\n" % err)
        sys.exit(-1)


if __name__ == "__main__":
    # get options, check and parse config file and send message
    options = parse_cmd_line()
    send_message(parse_config(check_config_file(options.config)), options.recipient, options.message)
