from widark import (
    Frame, Listbox, Label, Entry,
    Event, Modal, Button, Spacer, Color)
from .policies import PoliciesModal


class RolesModal(Modal):
    def setup(self, **context) -> 'RolesModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.dominion = context['dominion']
        self.role = None
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None
        frame = Frame(self, title=f'{self.dominion["name"]} Roles'
                      ).title_style(Color.WARNING()).weight(4, 2)

        Button(frame, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Button(frame, content='\U00002716 Cancel',
               command=self.on_cancel).style(Color.WARNING()).grid(0, 1)
        Listbox(frame, data=['Name', 'Description'],
                orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(
            frame, command=self.on_body).grid(3).span(col=3).weight(9)

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        if event.details['result'] == 'policies':
            self.modal = PoliciesModal(
                self, injector=self.injector,
                role=self.role,
                proportion={'height': 0.90, 'width': 0.95},
                done_command=self.on_modal_done).launch()
        elif event.details['result'] == 'users':
            self.modal = UsersSelectionModal(
                self, injector=self.injector,
                role=self.role,
                proportion={'height': 0.90, 'width': 0.95},
                done_command=self.on_modal_done).launch()
        else:
            await self.load()
        self.render()

    async def load(self) -> None:
        roles = await self.authark_informer.search(
            'role', [('dominion_id', '=', self.dominion['id'])])
        self.body.setup(data=roles, fields=['name', 'description'],
                        limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.role = getattr(event.target.parent, 'item', None)
        if self.role:
            self.modal = RoleDetailsModal(
                self, injector=self.injector, role=self.role,
                done_command=self.on_modal_done,
                proportion={'height': 0.50, 'width': 0.70}).launch()

    async def on_create(self, event: Event) -> None:
        role = {'id': '', 'name': '', 'dominion_id': self.dominion['id'],
                'description': ''}
        self.modal = RoleDetailsModal(
            self, injector=self.injector, role=role,
            done_command=self.on_modal_done,
            proportion={'height': 0.70, 'width': 0.70}).launch()

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})


class RoleDetailsModal(Modal):
    def setup(self, **context) -> 'RoleDetailsModal':
        self.injector = context['injector']
        self.management_manager = self.injector['ManagementManager']
        self.role = context['role']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Role').title_style(Color.SUCCESS()).weight(3, 2)
        Label(frame, content='Name:').grid(0, 0)
        self.name = Entry(frame, content=self.role['name']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Description:').grid(1, 0)
        self.description = Entry(frame, content=self.role['description']).style(
            border=[0]).grid(1, 1).weight(col=2)
        Label(frame, content='ID:').grid(2, 0)
        Label(frame, content=f'{self.role["id"]}').grid(2, 1)

        menu = Frame(self, title='Menu').grid(col=1)
        Button(menu, content='Policies',
               command=self.on_policies).style(border=[0])
        Button(menu, content='Users',
               command=self.on_users).grid(1).style(
                   Color.SUCCESS(), border=[0])

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
        self.role.update(role)
        await self.management_manager.create_role([self.role])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.management_manager.remove_role([self.role['id']])
        await self.done({'result': 'deleted'})

    async def on_policies(self, event: Event) -> None:
        await self.done({'result': 'policies'})

    async def on_users(self, event: Event) -> None:
        await self.done({'result': 'users'})


class UsersSelectionModal(Modal):
    def setup(self, **context) -> 'RoleDetailsModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.role = context['role']
        self.focused = None
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title=f'Users for role: {self.role["name"]}').title_style(
                Color.SUCCESS()).style(border=[]).weight(3, 2)

        self.available = Listbox(
            frame, command=self.on_select).grid(col=0)

        self.chosen = Listbox(
            frame, command=self.on_select).grid(col=1)
        # Label(frame, content='Name:').grid(0, 0)
        # self.name = Entry(frame, content=self.role['name']).style(
        #     border=[0]).grid(0, 1).weight(col=2)
        # Label(frame, content='Description:').grid(1, 0)
        # self.description = Entry(frame, content=self.role['description']).style(
        #     border=[0]).grid(1, 1).weight(col=2)
        # Label(frame, content='ID:').grid(2, 0)
        # Label(frame, content=f'{self.role["id"]}').grid(2, 1)

        # menu = Frame(self, title='Menu').grid(col=1)
        # Button(menu, content='Policies',
        #        command=self.on_policies).style(border=[0])
        # Button(menu, content='Users',
        #        command=self.on_users).grid(1).style(
        #            Color.SUCCESS(), border=[0])

        # actions = Frame(
        #     self, title='Actions').title_style(
        #         Color.WARNING()).grid(1).span(col=2)
        # Button(actions, content='Delete', command=self.on_delete
        #        ).style(Color.DANGER()).grid(0, 1)
        # Spacer(actions).grid(0, 2).weight(col=2)
        # Button(actions, content='Save', command=self.on_save
        #        ).style(Color.SUCCESS()).grid(0, 3)
        # Button(actions, content='Cancel', command=self.on_cancel
        #        ).style(Color.WARNING()).grid(0, 4)

    async def on_select(self, event: Event) -> None:
        item = getattr(event.target.parent, 'item', None)
        event.target.focus()

    async def load(self) -> None:
        # available = await self.authark_informer.search(
        #     'user', [('', '=', self.dominion['id'])])

        current_user_ids = [ranking['user_id'] for ranking in
                            await self.authark_informer.search('ranking', [
                                ('role_id', '=', self.role['id'])])]

        available_users = await self.authark_informer.search('user', [
            '!', ('id', 'in', current_user_ids)])

        self.available.setup(data=available_users,
                             fields=['id' 'name', 'email'], limit=20).connect()

    # async def on_cancel(self, event: Event) -> None:
    #     await self.done({'result': 'cancelled'})

    # async def on_delete(self, event: Event) -> None:
    #     await self.management_manager.remove_role([self.role['id']])
    #     await self.done({'result': 'deleted'})

    # async def on_policies(self, event: Event) -> None:
    #     await self.done({'result': 'policies'})

    # async def on_users(self, event: Event) -> None:
    #     await self.done({'result': 'users'})
