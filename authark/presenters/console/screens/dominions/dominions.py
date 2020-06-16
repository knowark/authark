from widark import (
    Frame, Listbox, Listitem, Label, Entry,
    Event, Modal, Button, Spacer, Color)
from .roles import RolesModal


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
        Label(self, content='\U0001F50D Search:').grid(0, 1)
        self.search = Entry(self, content=' ').grid(0, 2).style(
            border=[0]).weight(col=3)
        self.header = Listbox(
            self, data=['ID', 'Name', 'URL'],
            orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(
            self, command=self.on_body,
        ).grid(3).span(col=3).weight(9)

        self.listen('click', self.on_backdrop_click, True)

    async def load(self) -> None:
        dominions = await self.authark_informer.search('dominion')
        self.body.setup(
            data=dominions, fields=['id', 'name', 'url'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.dominion = getattr(event.target.parent, 'item', None)
        if self.dominion:
            self.modal = DominionDetailsModal(
                self, injector=self.injector, item=self.dominion,
                done_command=self.on_modal_done,
                proportion={'height': 0.50, 'width': 0.70}).launch()

    async def on_create(self, event: Event) -> None:
        dominion = {'name': '', 'url': ''}
        self.modal = DominionDetailsModal(
            self, injector=self.injector, item=dominion,
            done_command=self.on_modal_done,
            proportion={'height': 0.50, 'width': 0.50}).launch()

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        if event.details['result'] == 'roles':
            self.modal = RolesModal(
                self, injector=self.injector,
                dominion=self.dominion,
                done_command=self.on_modal_done).launch().connect()
        else:
            await self.load()
        self.render()

    async def on_backdrop_click(self, event: Event) -> None:
        if self.modal and not self.modal.hit(event):
            event.stop = True
            self.remove(self.modal)
            self.modal = None
            await self.load()
            self.render()


class DominionDetailsModal(Modal):
    def setup(self, **context) -> 'DominionDetailsModal':
        self.injector = context['injector']
        self.management_manager = self.injector['ManagementManager']
        self.item = context['item']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Dominion').title_style(Color.SUCCESS()).weight(4, 2)
        Label(frame, content='Name:').grid(0, 0)
        self.name = Entry(frame, content=self.item['name']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='URL:').grid(1, 0)
        self.url = Entry(frame, content=self.item['url']).style(
            border=[0]).grid(1, 1).weight(col=2)

        menu = Frame(self, title='Menu').grid(col=1)
        Button(menu, content='Roles', command=self.on_roles).style(border=[0])
        Spacer(menu).grid(1)

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
            'name': self.name.text,
            'url': self.url.text
        }
        self.item.update(dominion)
        await self.management_manager.create_dominion([self.item])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.management_manager.remove_dominion([self.item['id']])
        await self.done({'result': 'deleted'})

    async def on_roles(self, event: Event) -> None:
        await self.done({'result': 'roles'})
