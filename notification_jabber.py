#!/usr/bin/env python

# -*- coding: utf-8 -*-

# notification_jabber
# notification_jabber.py

try:
    import sys
    import os
    import ConfigParser
    from optparse import OptionParser
    import xmpp
except ImportError, err:
    print "ERROR: Couldn't load module. %s" % (err)
    sys.exit(0)


__author__ = "Alexei Andrushievich"
__email__ = "vint21h@vint21h.pp.ua"
__licence__ = "GPLv2 or later"
__description__ = "Notifications via jabber Nagios plugin"
__url__ = "https://github.com/vint21h/notification_jabber"
VERSION = (0, 2, 1)
__version__ = '.'.join(map(str, VERSION))


def parse_cmd_line():
    """
    Commandline options arguments parsing.
    """

    # build options and help
    version = "%%prog %s" % (__version__)
    parser = OptionParser(version=version)
    parser.add_option("-r", "--recipient", action="store", dest="recipient",
                                        default="", metavar="RECIPIENT",
                                        help="message recipient Jabber ID")
    parser.add_option("-m", "--message", metavar="MESSAGE", action="store",
                                        type="string", dest="message",
                                        default="", help="message text")
    parser.add_option("-c", "--config", metavar="CONFIG", action="store",
                                        type="string", dest="config",
                                        help="path to config file")
    parser.add_option("-q", "--quiet", metavar="QUIET", action="store_false",
                                        default=False, dest="quiet",
                                        help="path to config file")

    options = parser.parse_args(sys.argv)[0]

    # check mandatory command line options supplied
    mandatories = ["recipient", "message", ]
    for mandatory in mandatories:
        if not options.__dict__[mandatory]:
            print "Mandatory command line option '%s' is missing." % mandatory
            exit(0)

    return options


def check_config_file(ini):
    """
    Check config exist.
    """

    default_ini = "notification_jabber.ini"
    if ini and os.path.exists(ini):  # user config file path
        return ini
    elif os.path.exists(default_ini):  # default config file path
        return default_ini
    elif os.path.exists(os.path.join("/etc", default_ini)):  # default config file path in /etc
        return os.path.join("/etc", default_ini)
    else:
        print "ERROR: Config file %s don't exist" % (ini)
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
    for mandatory in mandatories:
        if not configdata[mandatory]:
            print "Mandatory config option '%s' is missing." % mandatory
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
    except Exception:
        print "ERROR: Couldn't connect or auth on server."
        sys.exit(-1)
    xmessage = xmpp.Message(recipient, message)
    xmessage.setAttr('type', 'chat')
    try:
        client.send(xmessage)
    except Exception:
        print "ERROR: Couldn't send message."
        sys.exit(-1)


if __name__ == "__main__":
    # get options, check and parse config file and send message
    options = parse_cmd_line()
    send_message(parse_config(check_config_file(options.config)), options.recipient, options.message)
