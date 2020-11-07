# -*- coding: utf-8 -*-

# nagios-notification-jabber
# tests/notification_jabber_test.py


from __future__ import unicode_literals

from io import StringIO
from argparse import Namespace

import pytest
import contextlib2


try:
    from pytest_mock.plugin import MockerFixture  # pylint: disable=W0611  # noqa: F401
except ImportError:
    from pytest_mock.plugin import (  # type: ignore  # pylint: disable=W0611  # noqa: F401,E501
        MockFixture as MockerFixture,
    )

from notification_jabber import NotificationJabber


__all__ = [
    "test__get_options",
    "test__get_options__missing_recipient_option",
    "test__get_options__missing_message_option",
]


def test__get_options(mocker):
    """
    Test "_get_options" method must return argparse namespace.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    mocker.patch(
        "sys.argv",
        [
            "notification_jabber.py",
            "-r",
            "test@example.com",
            "-t",
            "chat",
            "-m",
            "TEST",
            "-c",
            "notification_jabber.ini",
        ],
    )
    mocker.patch(
        "notification_jabber.NotificationJabber._get_config",
        return_value={
            "jid": "test@example.com",
            "password": "secret",
            "resource": "",
        },
    )
    notifier = NotificationJabber()

    assert isinstance(notifier.options, Namespace)  # nosec: B101


def test__get_options__missing_recipient_option(mocker):
    """
    Test "_get_options" method must exit with recipient option missing error.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    out = StringIO()
    mocker.patch("sys.argv", ["notification_jabber.py"])

    with pytest.raises(SystemExit):
        with contextlib2.redirect_stderr(out):
            NotificationJabber()

    assert "Required recipient option missing" in out.getvalue().strip()  # nosec: B101


def test__get_options__missing_message_option(mocker):
    """
    Test "_get_options" method must exit with message option missing error.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    out = StringIO()
    mocker.patch("sys.argv", ["notification_jabber.py", "-r", "test@example.com"])

    with pytest.raises(SystemExit):
        with contextlib2.redirect_stderr(out):
            NotificationJabber()

    assert "Required message option missing" in out.getvalue().strip()  # nosec: B101
