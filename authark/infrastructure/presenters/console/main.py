from widark import Application, Event, Frame, Color, Listbox, Spacer
from .screens import UsersScreen


class ConsoleApplication(Application):
    def setup(self, **context) -> 'ConsoleApplication':
        self.config = context.get('config')
        self.injector = context.get('injector')
        return super().setup(**context) and self

    async def prepare(self) -> None:
        self.tenancy_supplier = self.injector['TenantSupplier']
        self.session_manager = self.injector['SessionManager']
        first_tenant = next(iter(self.tenancy_supplier.search_tenants([])))
        self.session_manager.set_tenant(first_tenant)

    def build(self) -> None:
        self._build_menu()
        self.status = Frame(self, title='Status').title_style(
            Color.WARNING()).style(border=[0]).grid(0, 1).weight(1, 6)
        self.content = Frame(self, border=[0]).title_style(
            Color.SUCCESS()).style(border=[]).grid(1, 1).weight(6, 6)

    def _build_menu(self) -> None:
        self.menu = Frame(self, title='Menu').title_style(
            Color.PRIMARY()).style(border=[0]).span(2)
        Listbox(self.menu, data=['\U0001F6B9 Users', '\U0001F3DA Dominions'],
                command=self.on_menu_click)
        Spacer(self.menu).grid(1).weight(2)

    async def on_menu_click(self, event: Event) -> None:
        option = event.target
        if option.content == '\U0001F6B9 Users':
            self.content.clear()
            UsersScreen(self.content, injector=self.injector).connect()
        elif option.row.pos == 1:
            # print('Dominions')
            pass
