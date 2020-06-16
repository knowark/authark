import json
from widark import (
    Frame, Listbox, Label, Entry, Event, Modal, Button, Spacer, Color)
from .rankings import RankingsModal


class UsersScreen(Frame):
    def setup(self, **context) -> 'UsersScreen':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.user = None
        return super().setup(**context) and self

    def build(self) -> None:
        self.modal = None
        self.title = 'Users'
        self.style(Color.SUCCESS())
        Button(self, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Label(self, content='\U0001F50D Search:').grid(0, 1)
        self.search = Entry(self, content=' ').grid(0, 2).style(
            border=[0]).weight(col=3)
        self.header = Listbox(
            self, data=['ID', 'Name', 'Email'],
            orientation='horizontal').grid(1).span(col=3)
        self.body = Listbox(
            self, command=self.on_body).grid(3).span(col=3).weight(9)
        self.listen('click', self.on_backdrop_click, True)

    async def load(self) -> None:
        users = await self.authark_informer.search('user')
        self.body.setup(
            data=users, fields=['id', 'name', 'email'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.user = getattr(event.target.parent, 'item', None)
        if self.user:
            self.modal = UserDetailsModal(
                self, injector=self.injector, item=self.user,
                done_command=self.on_modal_done,
                proportion={'height': 0.90, 'width': 0.90}).launch()

    async def on_create(self, event: Event) -> None:
        item = {'name': '', 'username': '', 'email': '', 'attributes': '{}'}
        self.modal = UserDetailsModal(
            self, injector=self.injector, item=item,
            done_command=self.on_modal_done,
            proportion={'height': 0.90, 'width': 0.90}).launch()

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        if event.details['result'] == 'roles':
            self.modal = RankingsModal(
                self, injector=self.injector,
                user=self.user,
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


class UserDetailsModal(Modal):
    def setup(self, **context) -> 'UserDetailsModal':
        self.auth_manager = context['injector']['AuthManager']
        self.item = context['item']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        frame = Frame(
            self, title='User').title_style(Color.SUCCESS()).weight(6, 3)
        Label(frame, content='Name:').grid(0, 0)
        self.name = Entry(frame, content=self.item['name']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Username:').grid(1, 0)
        self.username = Entry(frame, content=self.item['username']).style(
            border=[0]).grid(1, 1).weight(col=2)
        Label(frame, content='Email:').grid(2, 0)
        self.email = Entry(frame, content=self.item['email']).style(
            border=[0]).grid(2, 1).weight(col=2)
        Label(frame, content='Password:').grid(3, 0)
        self.password = Entry(frame, content=' ').style(
            border=[0]).grid(3, 1).weight(col=2)
        Label(frame, content='Attributes:').grid(4, 0)

        attributes = {}
        try:
            attributes = json.loads(self.item['attributes'])
        except json.JSONDecodeError:
            pass

        self.attributes = Entry(
            frame, content=json.dumps(attributes, indent=4)).style(
            border=[0]).grid(4, 1).weight(4, 2)

        menu = Frame(self, title='Menu').grid(col=1)
        Button(menu, content='Roles', command=self.on_roles).style(border=[0])
        Spacer(menu).grid(1).weight(2)

        actions = Frame(self, title='Actions').title_style(
            Color.WARNING()).grid(1).span(col=2)
        Button(actions, content='Delete', command=self.on_delete
               ).style(Color.DANGER()).grid(0, 1)
        Spacer(actions).grid(0, 2).weight(col=2)
        Button(actions, content='Save', command=self.on_save
               ).style(Color.SUCCESS()).grid(0, 3)
        Button(actions, content='Cancel', command=self.on_cancel
               ).style(Color.WARNING()).grid(0, 4)

    async def on_save(self, event: Event) -> None:
        user = {
            'name': self.name.text,
            'username': self.username.text,
            'email': self.email.text,
            'attributes': self.attributes.text
        }
        if self.password.text.strip():
            user['password'] = self.password.text.strip()
        self.item.update(user)
        await self.auth_manager.update([self.item])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.auth_manager.deregister([self.item['id']])
        await self.done({'result': 'deleted'})

    async def on_roles(self, event: Event) -> None:
        await self.done({'result': 'roles'})