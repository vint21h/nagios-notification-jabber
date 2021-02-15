# -*- coding: utf-8 -*-

# nagios-notification-jabber
# tests/notification_jabber_test.py


from io import StringIO
from argparse import Namespace
from unittest.mock import mock_open
from typing import List  # pylint: disable=W0611

import pytest
import contextlib2
from pytest_mock.plugin import MockerFixture  # pylint: disable=W0611  # noqa: F401

from notification_jabber import NotificationJabber


__all__ = [
    "test__get_options",
    "test__get_options__missing_recipient_option",
    "test__get_options__missing_message_option",
    "test__get_config",
    "test__get_config__error",
    "test__get_config__no_section_option_error",
    "test__get_config__no_config_error",
]  # type: List[str]


def test__get_options(mocker: MockerFixture) -> None:
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


def test__get_options__missing_recipient_option(mocker: MockerFixture) -> None:
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


def test__get_options__missing_message_option(mocker: MockerFixture) -> None:
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


def test__get_config(mocker: MockerFixture) -> None:
    """
    Test "_get_config" method must return config data.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    data = """
    [JABBER]
    jid = test@example.com
    password = secret
    resource =
    """
    expected = {
        "jid": "test@example.com",
        "password": "secret",
        "resource": "",
    }
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
        "builtins.open",
        mock_open(read_data=data),
    )
    notifier = NotificationJabber()

    assert notifier.config == expected  # nosec: B101


def test__get_config__error(mocker: MockerFixture) -> None:
    """
    Test "_get_config" method must fail on an error.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    out = StringIO()
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
        "builtins.open",
        return_value=IOError(),
    )

    with pytest.raises(SystemExit):
        with contextlib2.redirect_stderr(out):
            NotificationJabber()

    assert (  # nosec: B101
        "ERROR: Config file read notification_jabber.ini error."
        in out.getvalue().strip()
    )


def test__get_config__no_section_option_error(mocker: MockerFixture) -> None:
    """
    Test "_get_config" method must fail on no section/option error.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    out = StringIO()
    data = """
    [JABBER]
    password = secret
    resource =
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
        "builtins.open",
        mock_open(read_data=data),
    )

    with pytest.raises(SystemExit):
        with contextlib2.redirect_stderr(out):
            NotificationJabber()

    assert (  # nosec: B101
        "ERROR: Config file missing section/option error." in out.getvalue().strip()
    )


def test__get_config__no_config_error(mocker: MockerFixture) -> None:
    """
    Test "_get_config" method must fail on no config file error.

    :param mocker: mock
    :type mocker: MockerFixture
    """

    out = StringIO()
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
        ],
    )

    with pytest.raises(SystemExit):
        with contextlib2.redirect_stderr(out):
            NotificationJabber()

    assert (  # nosec: B101
        "ERROR: Config file /etc/nagios/notification_jabber.ini does not exist"
        in out.getvalue().strip()
    )
