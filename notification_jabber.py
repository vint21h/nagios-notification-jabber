#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
#
# notification_jabber
# Copyright (C) 2011  vint21h.pp.ua
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

try:
	import sys
	import os
	import ConfigParser
	import xmpp
	import urllib
except ImportError, err:
	sys.stderr.write("ERROR: Couldn't load module %s", (err))
	sys.exit(0)

"""Package versioning
"""

__author__ = "vINT 21h <vint21h@vint21h.pp.ua>"
__version__ = "0.001"

"""Global variables
"""

__ini = "notification_jabber.ini"

"""Check config exist
"""

if os.path.exists(os.path.join("/etc", __ini)):
	__configIni = os.path.join("/etc", __ini)
elif os.path.exists(os.path.join(os.getcwd(), __ini)):
	__configIni = os.path.join(os.getcwd(), __ini)
else:
	print sys.stderr.write("ERROR: Config file don't exist")
	sys.exit(0)

"""Check command line parameters supplied and get it
"""

if len(sys.argv) < 3:
	sys.stderr.write ("Usage...\n %s [recipient] [message]\n", (sys.argv[0]))

"""Get connection settings from config file
"""

__config = ConfigParser.ConfigParser()
__config.read(__configIni)
__server = __config.get('Jabber', 'server')
__login = __config.get('Jabber', 'login')
__password = __config.get('Jabber', 'password')


