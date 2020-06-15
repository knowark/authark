from widark import (
    Frame, Listbox, Listitem, Label, Entry,
    Event, Modal, Button, Spacer, Color)


class RolesModal(Modal):
    def setup(self, **context) -> 'RolesModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.dominion = context['dominion']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        frame = Frame(
            self, title='Roles').title_style(Color.WARNING()).weight(4, 2)

        Button(frame, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        self.header = Listbox(
            frame, data=['ID', 'Name', 'Description'],
            orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(frame).grid(3).span(col=3).weight(9)

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        await self.load()
        self.render()

    async def load(self) -> None:
        roles = await self.authark_informer.search(
            'role', [('dominion_id', '=', self.dominion['id'])])
        self.body.setup(data=roles, fields=['id', 'name', 'description'],
                        limit=10).connect()

    async def on_create(self, event: Event) -> None:
        role = {'name': '', 'url': '', 'dominion_id': self.dominion['id']}
        self.modal = RoleDetailsModal(
            self, injector=self.injector, item=role,
            done_command=self.on_modal_done,
            proportion={'height': 0.70, 'width': 0.70}).launch()


class RoleDetailsModal(Modal):
    def setup(self, **context) -> 'RoleDetailsModal':
        self.injector = context['injector']
        self.management_manager = self.injector['ManagementManager']
        self.item = context['item']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Role').title_style(Color.SUCCESS()).weight(3, 2)
        Label(frame, content='Name:').grid(0, 0)
        self.name = Entry(frame, content=self.item['name']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Description:').grid(1, 0)
        self.description = Entry(frame, content=self.item['url']).style(
            border=[0]).grid(1, 1).weight(col=2)

        actions = Frame(
            self, title='Actions').title_style(
                Color.WARNING()).grid(1).span(col=2)
        Button(actions, content='Delete', command=self.on_delete
               ).style(Color.DANGER()).grid(0, 1)
        Spacer(actions).grid(0, 2).weight(col=2)
        Button(actions, content='Save', command=self.on_save
               ).style(Color.SUCCESS()).grid(0, 3)
        Button(actions, content='Cancel', command=self.on_cancel
               ).style(Color.WARNING()).grid(0, 4)

    async def on_save(self, event: Event) -> None:
        role = {
            'name': self.name.text,
            'description': self.description.text
        }
        self.item.update(role)
        await self.management_manager.create_role([self.item])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.management_manager.remove_role([self.item['id']])
        await self.done({'result': 'deleted'})

    async def on_roles(self, event: Event) -> None:
        await self.done({'result': 'roles'})
