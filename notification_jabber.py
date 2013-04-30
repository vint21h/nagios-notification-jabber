#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-jabber
# notification_jabber.py

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
    import warnings
    import ConfigParser
    from optparse import OptionParser
    # strong hack to supress deprecation warnings called by xmpppy using md5, sha modules and socket.ssl() method
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import xmpp
except ImportError, err:
    sys.stderr.write("ERROR: Couldn't load module. %s\n" % err)
    sys.exit(-1)

__all__ = ['parse_options', 'parse_config', 'send_message', 'main', ]

# metadata
__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv3 or later"
__description__ = "Notifications via jabber Nagios plugin"
__url__ = "https://github.com/vint21h/nagios-notification-jabber"
VERSION = (0, 6, 4)
__version__ = '.'.join(map(str, VERSION))


def parse_options():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % __version__
    parser = OptionParser(version=version)
    parser.add_option(
        "-r", "--recipient", action="store", dest="recipient",
        type="string", default="", metavar="RECIPIENT",
        help="message recipient Jabber ID"
    )
    parser.add_option(
        "-m", "--message", metavar="MESSAGE", action="store",
        type="string", dest="message", default="", help="message text"
    )
    parser.add_option(
        "-c", "--config", metavar="CONFIG", action="store",
        type="string", dest="config", default="/etc/notification_jabber.ini",
        help="path to config file"
    )
    parser.add_option(
        "-q", "--quiet", metavar="QUIET", action="store_true",
        default=False, dest="quiet", help="be quiet"
    )

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    mandatories = ["recipient", "message", ]
    if not all(options.__dict__[mandatory] for mandatory in mandatories):
        parser.error("Required command line option missing")

    return options


def parse_config(options):
    """
    Get connection settings from config file.
    """

    if os.path.exists(options.config):
        config = ConfigParser.ConfigParser()
        try:
            config.read(options.config)
        except Exception:
            if not options.quiet:
                sys.stderr.write("ERROR: Config file read %s error." % options.config)
            sys.exit(-1)

        try:
            configdata = {
                'jid': config.get('JABBER', 'jid'),
                'password': config.get('JABBER', 'password'),
                'resource': config.get('JABBER', 'resource'),
            }
        except ConfigParser.NoOptionError, err:
            sys.stderr.write("ERROR: Config file missing option error. %s\n" % err)
            sys.exit(-1)

        # check mandatory config options supplied
        mandatories = ["jid", "password", ]
        if not all(configdata[mandatory] for mandatory in mandatories):
            if not options.quiet:
                sys.stdout.write("Required config option missing\n")
            sys.exit(0)

        return configdata
    else:
        if not options.quiet:
            sys.stderr.write("ERROR: Config file %s does not exist\n" % options.config)
        sys.exit(0)


def send_message(config, options):
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
        if not options.quiet:
            sys.stdout.write("ERROR: Couldn't connect or auth on server. %s\n" % err)
        sys.exit(-1)
    xmessage = xmpp.Message(options.recipient, options.message)
    xmessage.setAttr('type', 'chat')
    try:
        client.send(xmessage)
    except Exception, err:
        if not options.quiet:
            sys.stdout.write("ERROR: Couldn't send message. %s\n" % err)
        sys.exit(-1)


def main():
    """
    Program main.
    """

    options = parse_options()
    send_message(parse_config(options), options)
    sys.exit(0)

if __name__ == "__main__":
    main()
