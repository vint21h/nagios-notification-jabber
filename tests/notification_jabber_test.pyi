# -*- coding: utf-8 -*-

# nagios-notification-jabber
# tests/notification_jabber_test.pyi

from typing import List  # pylint: disable=W0611

try:
    from pytest_mock.plugin import MockerFixture  # pylint: disable=W0611  # noqa: F401
except ImportError:
    from pytest_mock.plugin import (  # type: ignore  # pylint: disable=W0611  # noqa: F401,E501
        MockFixture as MockerFixture,
    )

__all__: List[str] = ...

def test__get_options(mocker: MockerFixture) -> None: ...
def test__get_options__missing_recipient_option(mocker: MockerFixture) -> None: ...
def test__get_options__missing_message_option(mocker: MockerFixture) -> None: ...
