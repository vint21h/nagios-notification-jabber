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
from argparse import Namespace, ArgumentParser  # pylint: disable=W0611  # noqa: F401

from xmpp import JID, Client, Message, Presence


try:
    from configparser import ConfigParser, NoOptionError, NoSectionError
except ImportError:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError  # type: ignore


__all__ = [
    "main",
]


# metadata
VERSION = (0, 8, 0)
__version__ = ".".join(map(str, VERSION))


class NotificationJabber(object):
    """
    Notifications via jabber Nagios plugin.
    """

    MESSAGE_TYPE_CHAT = "chat"  # type: str
    MESSAGE_TYPE_GROUP_CHAT = "groupchat"  # type: str

    def __init__(self):
        """
        Get command line args.
        """

        self.options = self._get_options()  # type: ignore
        self.config = self._get_config()  # type: ignore

    def _get_options(self):
        """
        Parse commandline options arguments.

        :return: parsed command line arguments
        :rtype: Namespace
        """

        parser = ArgumentParser(description="Notifications via jabber Nagios plugin")
        parser.add_argument(
            "-r",
            "--recipient",
            action="store",
            dest="recipient",
            type=str,
            default="",
            metavar="RECIPIENT",
            help="message recipient Jabber ID or Jabber MUC ID",
        )
        parser.add_argument(
            "-m",
            "--message",
            metavar="MESSAGE",
            action="store",
            type=str,
            dest="message",
            default="",
            help="message text",
        )
        parser.add_argument(
            "-t",
            "--message-type",
            metavar="TYPE",
            action="store",
            type=str,
            dest="type",
            default=self.MESSAGE_TYPE_CHAT,
            choices=[self.MESSAGE_TYPE_CHAT, self.MESSAGE_TYPE_GROUP_CHAT],
            help="message type ('{chat}' or '{group-chat}')".format(
                **{
                    "chat": self.MESSAGE_TYPE_CHAT,
                    "group-chat": self.MESSAGE_TYPE_GROUP_CHAT,
                }
            ),
        )
        parser.add_argument(
            "-c",
            "--config",
            metavar="CONFIG",
            action="store",
            type=str,
            dest="config",
            default="/etc/nagios/notification_jabber.ini",
            help="path to config file",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            default=False,
            dest="quiet",
            help="be quiet",
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version="{version}".format(version=__version__),
        )

        options = parser.parse_args()

        # check mandatory command line options supplied
        if not options.recipient:
            parser.error(message="Required recipient option missing")
        if not options.message:
            parser.error(message="Required message option missing")

        return options

    def _get_config(self):
        """
        Get connection settings from config file.

        :return: connection settings
        :rtype: Dict[str, str]
        """

        if os.path.exists(self.options.config):
            config = ConfigParser()
            try:
                config.read(self.options.config)
            except Exception as error:
                if not self.options.quiet:
                    sys.stderr.write(
                        "ERROR: Config file read {config} error. {error}".format(
                            config=self.options.config, error=error
                        )
                    )
                sys.exit(-1)

            try:
                data = {
                    "jid": config.get("JABBER", "jid"),
                    "password": config.get("JABBER", "password"),
                    "resource": config.get("JABBER", "resource"),
                }
            except (NoOptionError, NoSectionError) as error:
                sys.stderr.write(
                    "ERROR: Config file missing section/option error. {error}\n".format(
                        error=error
                    )
                )
                sys.exit(-1)

            # check mandatory config options supplied
            if not data.get("jid", None):
                if not self.options.quiet:
                    sys.stdout.write("Required jid config option missing\n")
                sys.exit(0)
            if not data.get("password", None):
                if not self.options.quiet:
                    sys.stdout.write("Required password config option missing\n")
                sys.exit(0)

            return data
        else:
            if not self.options.quiet:
                sys.stderr.write(
                    "ERROR: Config file {config} does not exist\n".format(
                        config=self.options.config
                    )
                )
            sys.exit(0)

    def _get_connection(self):
        """
        Get and return connection to jabber server.

        :return: connection to jabber server
        :rtype: Client
        """

        jid = JID(self.config.get("jid", ""))  # JID object
        client = Client(jid.getDomain(), debug=[])

        try:
            client.connect()
            client.auth(
                user=jid.getNode(),
                password=self.config.get("password", ""),
                resource=self.config.get("resource", ""),
            )
            client.sendInitPresence(requestRoster=0)
        except Exception as error:
            if not self.options.quiet:
                sys.stdout.write(
                    "ERROR: Couldn't connect or auth on server. {error}\n".format(
                        error=error
                    )
                )
            sys.exit(-1)

        return client

    def _get_message(self):
        """
        Create and return message.

        :return: jabber message
        :rtype: Message
        """

        message = Message(self.options.recipient, self.options.message)
        message.setAttr("type", self.options.type)

        return message

    def notify(self):
        """
        Send message.
        """

        connection = self._get_connection()  # type: ignore
        message = self._get_message()  # type: ignore

        try:
            if self.options.type == self.MESSAGE_TYPE_GROUP_CHAT:
                connection.send(
                    Presence(
                        to="{recipient}/{jid}".format(
                            **{
                                "recipient": self.options.recipient,
                                "jid": self.config.get("jid", ""),
                            }
                        )
                    )
                )
                sleep(1)
            connection.send(message)
        except Exception as error:
            if not self.options.quiet:
                sys.stdout.write(
                    "ERROR: Couldn't send message. {error}\n".format(error=error)
                )
            sys.exit(-1)


def main():
    """
    Program main.
    """

    notifier = NotificationJabber()  # type: ignore
    notifier.notify()  # type: ignore


if __name__ == "__main__":

    main()  # type: ignore
