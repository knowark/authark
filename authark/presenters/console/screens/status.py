from widark import (
    Frame, Listbox, Label, Event, Modal, Button, Color)


class StatusScreen(Frame):
    def setup(self, **context) -> 'StatusScreen':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.tenancy_supplier = self.injector['TenantSupplier']
        self.session_manager = self.injector['SessionManager']
        return super().setup(**context) and self

    def build(self) -> None:
        self.title = 'Status'
        self.title_style(Color.WARNING()).style(border=[0])
        self.modal = None

        self.switch = Button(self, content='Switch',
                             command=self.on_switch).style(Color.SUCCESS())
        self.tenant_name = Label(self).grid(0, 1)
        self.tenant_slug = Label(self).grid(0, 2)
        self.root.listen('click', self.on_backdrop_click, True)

    async def load(self) -> None:
        tenant = self.session_manager.get_tenant()
        self.tenant_name.setup(content=tenant['name']).render()
        self.tenant_slug.setup(content=tenant['slug']).render()

    async def on_switch(self, event: Event) -> None:
        self.modal = TenantsModal(
            self.root, injector=self.injector,
            done_command=self.on_modal_done,
            proportion={'height': 0.60, 'width': 0.60}).launch().connect()

    async def on_modal_done(self, event: Event) -> None:
        if self.modal:
            self.root.remove(self.modal)
            self.modal = None
            await self.dispatch(Event(
                'Custom', 'tenant_switch', details=event.details))

    async def on_backdrop_click(self, event: Event) -> None:
        if self.modal and not self.modal.hit(event):
            event.stop = True
            self.root.remove(self.modal)
            self.modal = None
            self.root.render()


class TenantsModal(Modal):
    def setup(self, **context) -> 'TenantsModal':
        self.tenant_supplier = context['injector']['TenantSupplier']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.header = Listbox(self, data=['ID', 'Name'],
                              orientation='horizontal')
        self.body = Listbox(self, command=self.on_body).grid(1).weight(4)

    async def load(self) -> None:
        tenants = self.tenant_supplier.search_tenants([])
        self.body.setup(data=tenants, fields=['id', 'name']).connect()

    async def on_body(self, event: Event) -> None:
        item = event.target.parent.item
        await self.done(item)
