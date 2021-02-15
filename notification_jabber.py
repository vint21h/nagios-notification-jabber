#!/usr/bin/env python

# -*- coding: utf-8 -*-

# nagios-notification-jabber
# notification_jabber.py

# Copyright (c) 2011-2021 Alexei Andrushievich <vint21h@vint21h.pp.ua>
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


import os
import sys
from time import sleep
from typing import Dict, List  # pylint: disable=W0611
from configparser import ConfigParser, NoOptionError, NoSectionError
from argparse import Namespace, ArgumentParser  # pylint: disable=W0611  # noqa: F401

from xmpp import JID, Client, Message, Presence


__all__ = [
    "main",
]  # type: List[str]


# metadata
VERSION = (0, 8, 0)
__version__ = ".".join(map(str, VERSION))


class NotificationJabber(object):
    """
    Notifications via jabber Nagios plugin.
    """

    MESSAGE_TYPE_CHAT = "chat"  # type: str
    MESSAGE_TYPE_GROUP_CHAT = "groupchat"  # type: str

    def __init__(self) -> None:
        """
        Get command line args.
        """

        self.options = self._get_options()
        self.config = self._get_config()

    def _get_options(self) -> Namespace:
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

    def _get_config(self) -> Dict[str, str]:
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
                return {
                    "jid": config.get(section="JABBER", option="jid"),
                    "password": config.get(section="JABBER", option="password"),
                    "resource": config.get(section="JABBER", option="resource"),
                }
            except (KeyError, NoOptionError, NoSectionError) as error:
                sys.stderr.write(
                    "ERROR: Config file missing section/option error. {error}\n".format(
                        error=error
                    )
                )
                sys.exit(-1)

        else:
            if not self.options.quiet:
                sys.stderr.write(
                    "ERROR: Config file {config} does not exist\n".format(
                        config=self.options.config
                    )
                )
            sys.exit(0)

    def _get_connection(self) -> Client:
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

    def _get_message(self) -> Message:
        """
        Create and return message.

        :return: jabber message
        :rtype: Message
        """

        message = Message(self.options.recipient, self.options.message)
        message.setAttr("type", self.options.type)

        return message

    def notify(self) -> None:
        """
        Send message.
        """

        connection = self._get_connection()
        message = self._get_message()

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


def main() -> None:
    """
    Program main.
    """

    notifier = NotificationJabber()
    notifier.notify()


if __name__ == "__main__":

    main()
