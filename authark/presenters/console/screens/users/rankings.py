from typing import Dict
from widark import (Frame, Listbox, Event, Modal, Label, Button, Color)


class RankingsModal(Modal):
    def setup(self, **context) -> 'RankingsModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.user = context['user']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None
        frame = Frame(self, title='Rankings').title_style(
            Color.WARNING()).weight(4, 2)
        Button(frame, content='\U00002795 Assign',
               command=self.on_assign).grid(0, 0)
        Label(frame, content='"Shift + Click" to Delete').grid(0, 1)
        self.header = Listbox(
            frame, data=['ID', 'Role', 'Dominion'],
            orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(frame, command=self.on_body).grid(
            3).span(col=3).weight(9)

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        if event.details['result'] == 'roles':
            await self.assign_role(event.details['role'])
        else:
            await self.load()
        self.render()

    async def load(self) -> None:
        rankings = await self.authark_informer.search(
            'ranking', [('user_id', '=', self.user['id'])])
        roles_map = {
            role['id']: role for role
            in await self.authark_informer.search(
                'role', [('id', 'in', [
                    ranking['role_id'] for ranking in rankings])])}
        dominions_map = {
            dominion['id']: dominion for dominion
            in await self.authark_informer.search(
                'dominion', [('id', 'in', [
                    role['dominion_id'] for role in roles_map.values()])])}
        for ranking in rankings:
            role = roles_map[ranking['role_id']]
            ranking['role_name'] = role['name']
            ranking['dominion_name'] = dominions_map[
                role['dominion_id']]['name']

        self.body.setup(data=rankings, fields=[
            'id', 'role_name', 'dominion_name'], limit=10).connect()

    async def on_assign(self, event: Event) -> None:
        self.modal = RoleSelectionModal(
            self, injector=self.injector,
            done_command=self.on_modal_done,
            proportion={'height': 0.70, 'width': 0.70}).launch().connect()

    async def assign_role(self, role_dict: Dict[str, str]) -> None:
        ranking_dict = {'user_id': self.user['id'], 'role_id': role_dict['id']}
        await self.management_manager.assign_role([ranking_dict])
        self.connect()

    async def on_body(self, event: Event) -> None:
        ranking = getattr(event.target.parent, 'item', None)
        if ranking:
            await self.management_manager.deassign_role([ranking['id']])
            self.connect()


class RoleSelectionModal(Modal):
    def setup(self, **context) -> 'RoleSelectionModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        return super().setup(**context) and self

    def build(self) -> None:
        Listbox(self, data=['ID', 'Name', 'Dominion'],
                orientation='horizontal').grid(0)
        self.body = Listbox(self, command=self.on_body).grid(1).weight(9)

    async def load(self) -> None:
        roles = await self.authark_informer.search('role', [])
        dominions_map = {
            dominion['id']: dominion for dominion
            in await self.authark_informer.search(
                'dominion', [('id', 'in', [
                    role['dominion_id'] for role in roles])])}
        for role in roles:
            role['dominion_name'] = dominions_map[role['dominion_id']]['name']

        self.body.setup(data=roles,
                        fields=['id', 'name', 'dominion_name']).connect()

    async def on_body(self, event: Event) -> None:
        role = getattr(event.target.parent, 'item', None)
        if role:
            await self.done({'result': 'roles', 'role': role})
