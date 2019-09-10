import urwid
from typing import Set
from authark.infrastructure.terminal.framework import Table, Screen
from authark.infrastructure.terminal.screens.tenants.tenants_actions import (
    TenantsDetailsScreen)


def test_tenants_detail_screen(main):
    tenants_detail_screen = TenantsDetailsScreen(
        "TENANT'S DETAILS", main.env, None)
    assert not hasattr(tenants_detail_screen, "selected_item")
