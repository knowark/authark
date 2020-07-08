from authark.application.domain.models.entity import Entity
from typing import Dict, Optional, Any
from widark import (
    Frame, Listbox, Label, Entry,
    Event, Modal, Button, Spacer, Color)
from .policies import PoliciesModal


class RolesScreen(Frame):
    def setup(self, **context) -> 'RolesScreen':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.dominion = {}
        self.role = None
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None
        self.title = 'Roles'

        Button(self, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Button(self, content='Dominion',
               command=self.on_dominion).style(Color.SUCCESS()).grid(0, 1)
        self.dominion_label = Label(
            self, content=f'{self.dominion.get("name")}').grid(0, 2)
        Listbox(self, data=['Name', 'Description'],
                orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(
            self, command=self.on_body).grid(2).span(col=3).weight(9)

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
                proportion={'height': 0.95, 'width': 0.95},
                done_command=self.on_modal_done).launch()
        else:
            await self.load()
        self.render()

    async def load(self) -> None:
        self.dominion = self.dominion or next(iter(
            await self.authark_informer.search('dominion')), {'id': 'None'})
        roles = await self.authark_informer.search(
            'role', [('dominion_id', '=', self.dominion.get('id'))])
        self.body.setup(
            data=roles, fields=['name', 'description'], limit=20).connect()
        self.dominion_label.setup(
            content=f'{self.dominion.get("name")}').render()

    async def on_body(self, event: Event) -> None:
        self.role = getattr(event.target.parent, 'item', None)
        if self.role:
            self.modal = RoleDetailsModal(
                self, injector=self.injector, role=self.role,
                done_command=self.on_modal_done,
                proportion={'height': 0.67, 'width': 0.80}).launch()

    async def on_dominion(self, event: Event) -> None:
        self.modal = DominionsModal(
            self, injector=self.injector,
            done_command=self.on_dominion_switch,
            proportion={'height': 0.60, 'width': 0.80}
        ).launch()

    async def on_dominion_switch(self, event: Event) -> None:
        self.dominion = event.details
        self.connect()

    async def on_create(self, event: Event) -> None:
        role = {'id': '', 'name': '', 'dominion_id': self.dominion.get('id'),
                'description': ''}
        self.modal = RoleDetailsModal(
            self, injector=self.injector, role=role,
            done_command=self.on_modal_done,
            proportion={'height': 0.70, 'width': 0.70}).launch()

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})


class DominionsModal(Modal):
    def setup(self, **context) -> 'DominionsModal':
        self.authark_informer = context['injector']['AutharkInformer']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.header = Listbox(self, data=['ID', 'Name'],
                              orientation='horizontal')
        self.body = Listbox(self, command=self.on_body).grid(1).weight(4)

    async def load(self) -> None:
        dominions = await self.authark_informer.search('dominion')
        self.body.setup(data=dominions, fields=['id', 'name']).connect()

    async def on_body(self, event: Event) -> None:
        item = event.target.parent.item
        await self.done(item)


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
        self.focused = {}
        self.available_domain = []
        self.chosen_domain = []
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        available_frame = Frame(self, title='Available').weight(
            5, 4).grid(0, 0)
        self.available_search = Entry(
            available_frame, command=self.on_available_search).listen(
                'keydown', self.on_available_search, True).weight(
                    col=2).grid(0, 0)
        self.available_total = Label(
            available_frame, content='Total: 0').grid(0, 1)
        self.available = Listbox(
            available_frame, command=self.on_select).weight(
                9).span(col=2).grid(1)

        switchers = Frame(self).title_style(
            Color.SUCCESS()).style(border=[]).weight(5).grid(0, 1)

        Button(switchers, content='\U000025B6', command=self.on_choose).style(
            Color.SUCCESS(), border=[], template='{}').grid(0)
        Button(switchers, content='\U000025C0', command=self.on_clear).style(
            Color.SUCCESS(), border=[], template='{}').grid(1)
        Button(switchers, content='\U000023E9',
               command=self.on_choose_all).style(
            Color.SUCCESS(), border=[], template='{}').grid(2)
        Button(switchers, content='\U000023EA',
               command=self.on_clear_all).style(
            Color.SUCCESS(), border=[], template='{}').grid(3)

        chosen_frame = Frame(self, title='Chosen').weight(
            5, 4).grid(0, 2)
        self.chosen_search = Entry(chosen_frame).listen(
            'keydown', self.on_chosen_search, True).weight(col=2).grid(0, 0)
        self.chosen_total = Label(
            chosen_frame, content='Total: 0').grid(0, 1)
        self.chosen = Listbox(
            chosen_frame, command=self.on_select).weight(9).grid(1)

        actions = Frame(
            self, title='Actions').title_style(
                Color.WARNING()).grid(1).span(col=3)
        Label(actions, content=f'Role: {self.role["name"]}').grid(0, 2)
        Spacer(actions).grid(0, 3).weight(col=1)
        Button(actions, content='Save', command=self.on_save
               ).style(Color.SUCCESS()).grid(0, 4)
        Button(actions, content='Cancel', command=self.on_cancel
               ).style(Color.WARNING()).grid(0, 5)

    async def on_select(self, event: Event) -> None:
        item = getattr(event.target.parent, 'item', None)
        event.target.focus()
        self.focused = item if isinstance(item, dict) else None

    async def on_available_search(self, event: Event) -> None:
        if event.key == '\n':
            event.stop = True
            text = self.available_search.text.strip()
            self.available.offset = 0
            self.available_domain = [] if not text else [
                '|',  ('name', 'ilike', f'%{text}%'),
                ('email', 'ilike', f'%{text}%')]
            await self.load()
            self.available_search.focus()

    async def on_chosen_search(self, event: Event) -> None:
        if event.key == '\n':
            event.stop = True
            text = self.chosen_search.text.strip()
            self.chosen.offset = 0
            self.chosen_domain = [] if not text else [
                '|',  ('name', 'ilike', f'%{text}%'),
                ('email', 'ilike', f'%{text}%')]
            await self.load()
            self.chosen_search.focus()

    async def load(self) -> None:
        current_user_ids = [ranking['user_id'] for ranking in
                            await self.authark_informer.search('ranking', [
                                ('role_id', '=', self.role['id'])])]
        available_users = await self.authark_informer.search('user', [
            '!', ('id', 'in', current_user_ids)] + self.available_domain)
        chosen_users = await self.authark_informer.search('user', [
            ('id', 'in', current_user_ids)] + self.chosen_domain)

        self.available.setup(data=available_users,
                             fields=['username', 'email'],
                             limit=20).connect()
        self.chosen.setup(data=chosen_users,
                          fields=['username', 'email'],
                          limit=20).connect()
        self._update_totals()

    async def on_choose(self, event: Event) -> None:
        self._switch(self.focused, self.available, self.chosen)
        self._update_totals()

    async def on_choose_all(self, event: Event) -> None:
        for item in list(self.available.data):
            self._switch(item, self.available, self.chosen)
        self._update_totals()

    async def on_clear(self, event: Event) -> None:
        self._switch(self.focused, self.chosen, self.available)
        self._update_totals()

    async def on_clear_all(self, event: Event) -> None:
        for item in list(self.chosen.data):
            self._switch(item, self.chosen, self.available)
        self._update_totals()

    def _update_totals(self) -> None:
        self.available_total.setup(
            content=f'Total: {len(self.available.data)}').render()
        self.chosen_total.setup(
            content=f'Total: {len(self.chosen.data)}').render()

    def _switch(self, item: Optional[Dict[str, Any]],
                source: Listbox, target: Listbox) -> None:
        if item and item in source.data:
            source.data.remove(item)
            source.connect()
        if item and item not in target.data:
            target.data.insert(0, item)
            target.connect()

    async def on_save(self, event: Event) -> None:
        removing_ranking_ids = [
            ranking['id'] for ranking in await self.authark_informer.search(
                'ranking', [('role_id', '=', self.role['id']),
                            ('user_id', 'in', [user['id'] for user in
                                               self.available.data])])]
        await self.management_manager.deassign_role(removing_ranking_ids)
        adding_rankings = [{'role_id': self.role['id'], 'user_id': user['id']}
                           for user in self.chosen.data]
        await self.management_manager.assign_role(adding_rankings)
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})
