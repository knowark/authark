from typing import Dict, Any
from widark import Application, Event, Frame, Color, Listbox, Spacer
from .screens import UsersScreen, StatusScreen


class ConsoleApplication(Application):
    def setup(self, **context) -> 'ConsoleApplication':
        self.config = context['config']
        self.injector = context['injector']
        return super().setup(**context) and self

    async def prepare(self) -> None:
        tenancy_supplier = self.injector['TenantSupplier']
        tenants = tenancy_supplier.search_tenants([])
        tenant_dict = next(iter(tenants), {'name': 'None'})
        self._set_tenant(tenant_dict)

    def build(self) -> None:
        self._build_menu()
        self._build_status()
        self.content = Frame(self, border=[0]).title_style(
            Color.SUCCESS()).style(border=[]).grid(1, 1).weight(9, 5)

    async def on_menu_click(self, event: Event) -> None:
        option = event.target
        if option.content == '\U0001F6B9 Users':
            self.content.clear()
            UsersScreen(self.content, injector=self.injector).connect()
        elif option.row.pos == 1:
            # print('Dominions')
            pass

    async def on_tenant_switch(self, event: Event) -> None:
        if event.details.get('name'):
            self._set_tenant(event.details)
        self.connect()

    def _set_tenant(self, tenant_dict: Dict[str, Any]) -> None:
        session_manager = self.injector['SessionManager']
        session_manager.set_tenant(tenant_dict)

    def _build_status(self) -> None:
        self.status = StatusScreen(
            self, injector=self.injector).grid(0, 1).weight(1, 5)
        self.status.listen('tenant_switch', self.on_tenant_switch)

    def _build_menu(self) -> None:
        self.menu = Frame(self, title='Menu').title_style(
            Color.PRIMARY()).style(border=[0]).span(2)
        Listbox(self.menu, data=['\U0001F6B9 Users', '\U0001F3DA Dominions'],
                command=self.on_menu_click)
        Spacer(self.menu).grid(1).weight(2)
