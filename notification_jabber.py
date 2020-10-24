#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-jabber
# notification_jabber.py

# Copyright (c) 2011-2020 Alexei Andrushievich <vint21h@vint21h.pp.ua>
# Notifications via jabber Nagios plugin [https://github.com/vint21h/nagios-notification-jabber/]  # noqa: E501
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


from __future__ import unicode_literals

import os
import sys
from time import sleep
from optparse import OptionParser

import xmpp
import ConfigParser


__all__ = [
    "main",
]


# metadata
VERSION = (0, 8, 0)
__version__ = ".".join(map(str, VERSION))

# some global variables
CHAT, GROUP_CHAT = "chat", "groupchat"


def parse_options():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog {version}".format(version=__version__)
    parser = OptionParser(version=version)
    parser.add_option(
        "-r",
        "--recipient",
        action="store",
        dest="recipient",
        type="string",
        default="",
        metavar="RECIPIENT",
        help="message recipient Jabber ID or Jabber MUC ID",
    )
    parser.add_option(
        "-m",
        "--message",
        metavar="MESSAGE",
        action="store",
        type="string",
        dest="message",
        default="",
        help="message text",
    )
    parser.add_option(
        "-t",
        "--message-type",
        metavar="TYPE",
        action="store",
        type="string",
        dest="type",
        default=CHAT,
        help="message type ('{chat}' or '{groupchat}')".format(
            **{
                "chat": CHAT,
                "groupchat": GROUP_CHAT,
            }
        ),
    )
    parser.add_option(
        "-c",
        "--config",
        metavar="CONFIG",
        action="store",
        type="string",
        dest="config",
        default="/etc/nagios/notification_jabber.ini",
        help="path to config file",
    )
    parser.add_option(
        "-q",
        "--quiet",
        metavar="QUIET",
        action="store_true",
        default=False,
        dest="quiet",
        help="be quiet",
    )

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    if not all(
        options.__dict__[mandatory]
        for mandatory in [
            "recipient",
            "message",
            "type",
        ]
    ):
        parser.error("Required command line option missing")

    # check message type support
    if options.type not in [
        CHAT,
        GROUP_CHAT,
    ]:
        parser.error(
            "Type option must be {chat} or {groupchat}".format(
                **{
                    "chat": CHAT,
                    "groupchat": GROUP_CHAT,
                }
            )
        )

    return options


def parse_config(options):
    """
    Get connection settings from config file.
    """

    if os.path.exists(options.config):
        config = ConfigParser.ConfigParser()
        try:
            config.read(options.config)
        except Exception as error:
            if not options.quiet:
                sys.stderr.write(
                    "ERROR: Config file read {config} error. {error}".format(
                        config=options.config, error=error
                    )
                )
            sys.exit(-1)

        try:
            configdata = {
                "jid": config.get("JABBER", "jid"),
                "password": config.get("JABBER", "password"),
                "resource": config.get("JABBER", "resource"),
            }
        except ConfigParser.NoOptionError as error:
            sys.stderr.write(
                "ERROR: Config file missing option error. {error}\n".format(error=error)
            )
            sys.exit(-1)

        # check mandatory config options supplied
        mandatories = [
            "jid",
            "password",
        ]
        if not all(configdata[mandatory] for mandatory in mandatories):
            if not options.quiet:
                sys.stdout.write("Required config option missing\n")
            sys.exit(0)

        return configdata
    else:
        if not options.quiet:
            sys.stderr.write(
                "ERROR: Config file {config} does not exist\n".format(
                    config=options.config
                )
            )
        sys.exit(0)


def send_message(config, options):
    """
    Connect to server and send message.
    """

    jid = xmpp.JID(config["jid"])  # JID object
    client = xmpp.Client(jid.getDomain(), debug=[])
    try:
        client.connect()
        client.auth(jid.getNode(), config["password"], config["resource"])
        client.sendInitPresence(requestRoster=0)
    except Exception as error:
        if not options.quiet:
            sys.stdout.write(
                "ERROR: Couldn't connect or auth on server. {error}\n".format(
                    error=error
                )
            )
        sys.exit(-1)

    xmessage = xmpp.Message(options.recipient, options.message)
    xmessage.setAttr("type", options.type)

    try:
        if options.type == GROUP_CHAT:
            client.send(
                xmpp.Presence(
                    to="{recipient}/{jid}".format(
                        **{"recipient": options.recipient, "jid": config["jid"]}
                    )
                )
            )
            sleep(1)
        client.send(xmessage)
    except Exception as error:
        if not options.quiet:
            sys.stdout.write(
                "ERROR: Couldn't send message. {error}\n".format(error=error)
            )
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
