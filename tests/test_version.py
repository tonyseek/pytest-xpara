from __future__ import absolute_import

from pytest_xpara import __version__ as version


def test_version():
    assert version == '0.3.0'
