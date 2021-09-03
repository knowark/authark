from widark import (
    Frame, Listbox, Label, Event, Modal, Button, Spacer, Entry, Color)


class StatusScreen(Frame):
    def setup(self, **context) -> 'StatusScreen':
        self.injector = context['injector']
        self.authark_informer = self.injector['StandardInformer']
        self.tenancy_supplier = self.injector['TenantInformer']
        self.session_manager = self.injector['SessionManager']
        return super().setup(**context) and self

    def build(self) -> None:
        self.title = 'Status'
        self.title_style(Color.WARNING()).style(border=[0])
        self.modal = None

        self.provision = Button(
            self, content='Provision',
            command=self.on_provision).style(Color.LIGHT()).grid(0, 0)
        self.switch = Button(
            self, content='Switch',
            command=self.on_switch).style(Color.SUCCESS()).grid(0, 1)
        self.tenant_name = Label(self).grid(0, 2).weight(col=2)
        self.tenant_slug = Label(self).grid(0, 3).weight(col=2)

    async def load(self) -> None:
        user = self.session_manager.get_user()
        self.tenant_name.setup(content=user['organization']).render()
        self.tenant_slug.setup(content=user['tenant']).render()

    async def on_switch(self, event: Event) -> None:
        self.modal = TenantsModal(
            self.root, injector=self.injector,
            done_command=self.on_modal_done,
            proportion={'height': 0.60, 'width': 0.60}).launch()

    async def on_provision(self, event: Event) -> None:
        self.modal = TenantProvisionModal(
            self.root, injector=self.injector,
            done_command=self.on_modal_done,
            proportion={'height': 0.40, 'width': 0.60}).launch()

    async def on_modal_done(self, event: Event) -> None:
        self.root.remove(self.modal)
        self.modal = None
        await self.dispatch(Event(
            'Custom', 'tenant_switch', details=event.details))


class TenantsModal(Modal):
    def setup(self, **context) -> 'TenantsModal':
        self.tenant_supplier = context['injector']['TenantInformer']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.header = Listbox(self, data=['ID', 'Name'],
                              orientation='horizontal')
        self.body = Listbox(self, command=self.on_body).grid(1).weight(4)

    async def load(self) -> None:
        tenants = (await self.tenant_supplier.search_tenants({
            "meta": {
                "domain": []
            }
        }))['data']
        self.body.setup(data=tenants, fields=['id', 'name']).connect()

    async def on_body(self, event: Event) -> None:
        item = event.target.parent.item
        await self.done(item)


class TenantProvisionModal(Modal):
    def setup(self, **context) -> 'TenantsModal':
        self.tenant_supplier = context['injector']['TenantManager']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        frame = Frame(
            self, title='Tenant').weight(6).title_style(Color.LIGHT())
        Label(frame, content='ID:').grid(0, 0)
        self.id = Entry(frame, content=' ').style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Name:').grid(1, 0)
        self.name = Entry(frame, content=' ').style(
            border=[0]).grid(1, 1).weight(col=2)

        actions = Frame(
            self, title='Actions').grid(1).title_style(
                Color.WARNING()).weight(3)
        Spacer(actions).grid(0, 2).weight(col=2)
        Button(actions, content='Save', command=self.on_save
               ).style(Color.SUCCESS()).grid(0, 3)
        Button(actions, content='Cancel', command=self.on_cancel
               ).style(Color.WARNING()).grid(0, 4)

    async def on_save(self, event: Event) -> None:
        tenant = {'name': self.name.text.strip()}
        if self.id.text.strip():
            tenant['id'] = self.id.text.strip()

        self.tenant_supplier.create_tenant({
            "meta": {},
            "data": tenant
        })
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})
