from widark import (
    Frame, Listbox, Label, Entry,
    Event, Modal, Button, Spacer, Color)


class DominionsScreen(Frame):
    def setup(self, **context) -> 'DominionsScreen':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.dominion = None
        return super().setup(**context) and self

    def build(self) -> None:
        self.modal = None
        self.title = 'Dominions'
        self.style(Color.SUCCESS())
        Button(self, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Spacer(self).grid(0, 1).weight(col=2)
        self.header = Listbox(
            self, data=['ID', 'Name'],
            orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(
            self, command=self.on_body,
        ).grid(3).span(col=3).weight(9)

    async def load(self) -> None:
        dominions = await self.authark_informer.search('dominion')
        self.body.setup(
            data=dominions, fields=['id', 'name'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.dominion = getattr(event.target.parent, 'item', None)
        if self.dominion:
            self.modal = DominionDetailsModal(
                self, injector=self.injector, dominion=self.dominion,
                done_command=self.on_modal_done,
                proportion={'height': 0.67, 'width': 0.67}).launch()

    async def on_create(self, event: Event) -> None:
        dominion = {'name': ''}
        self.modal = DominionDetailsModal(
            self, injector=self.injector, dominion=dominion,
            done_command=self.on_modal_done,
            proportion={'height': 0.67, 'width': 0.67}).launch()

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        await self.load()
        self.render()


class DominionDetailsModal(Modal):
    def setup(self, **context) -> 'DominionDetailsModal':
        self.injector = context['injector']
        self.management_manager = self.injector['ManagementManager']
        self.dominion = context['dominion']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Dominion').title_style(Color.SUCCESS()).weight(4, 2)
        Label(frame, content='Name:').grid(0, 0)
        self.name = Entry(frame, content=self.dominion['name']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Spacer(frame).grid(2).span(col=2)

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
        dominion = {
            'name': self.name.text
        }
        self.dominion.update(dominion)
        await self.management_manager.create_dominion([self.dominion])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.management_manager.remove_dominion([self.dominion['id']])
        await self.done({'result': 'deleted'})

    async def on_roles(self, event: Event) -> None:
        await self.done({'result': 'roles'})
