from widark import (
    Frame, Listbox, Label, Entry,
    Event, Modal, Button, Spacer, Color)


class RestrictionsModal(Modal):
    def setup(self, **context) -> 'RestrictionsModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.security_manager = self.injector['SecurityManager']
        self.policy = context['policy']
        self.restriction = None
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None
        frame = Frame(
            self, title=f'Restrictions for resource: {self.policy["resource"]}'
        ).title_style(Color.WARNING()).weight(4, 2)

        Button(frame, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Button(frame, content='\U00002716 Cancel',
               command=self.on_cancel).style(Color.WARNING()).grid(0, 1)

        Listbox(frame, data=['Sequence', 'Name', 'Target', 'Domain'],
                orientation='horizontal').grid(1).span(col=3)
        self.body = Listbox(frame, command=self.on_body
                            ).grid(3).span(col=3).weight(9)

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        await self.load()
        self.render()

    async def load(self) -> None:
        roles = await self.authark_informer.search(
            'restriction', [('policy_id', '=', self.policy['id'])])
        self.body.setup(data=roles, fields=[
            'sequence', 'name', 'target', 'domain'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.restriction = getattr(event.target.parent, 'item', None)
        if self.restriction:
            self.modal = RestrictionDetailsModal(
                self, injector=self.injector, restriction=self.restriction,
                done_command=self.on_modal_done,
                proportion={'height': 0.85, 'width': 0.90}).launch()

    async def on_create(self, event: Event) -> None:
        restriction = {
            'id': '', 'policy_id': self.policy['id'], 'sequence': 0,
            'name': '', 'target': self.policy['resource'], 'domain': ''}
        self.modal = RestrictionDetailsModal(
            self, injector=self.injector, restriction=restriction,
            done_command=self.on_modal_done,
            proportion={'height': 0.85, 'width': 0.90}).launch()

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})


class RestrictionDetailsModal(Modal):
    def setup(self, **context) -> 'RestrictionDetailsModal':
        self.injector = context['injector']
        self.security_manager = self.injector['SecurityManager']
        self.restriction = context['restriction']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Restriction').title_style(
                Color.SUCCESS()).weight(4, 2)

        Label(frame, content='Sequence:').grid(0, 0)
        self.sequence = Entry(
            frame, content=str(self.restriction['sequence'])).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Name:').grid(1, 0)
        self.name = Entry(frame, content=self.restriction['name']).style(
            border=[0]).grid(1, 1).weight(col=2)
        Label(frame, content='Target:').grid(2, 0)
        self.target = Entry(
            frame, content=str(self.restriction['target'])).style(
            border=[0]).grid(2, 1).weight(col=2)
        Label(frame, content='Domain:').grid(3, 0)
        self.domain = Entry(
            frame, content=str(self.restriction['domain'])).style(
            border=[0]).grid(3, 1).weight(2, 2)
        Label(frame, content='ID:').grid(4, 0)
        Label(frame, content=f'{self.restriction["id"]}').grid(4, 1)

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
        restriction = {
            'sequence': int(self.sequence.text),
            'name': self.name.text,
            'target': self.target.text,
            'domain': self.domain.text,
        }

        self.restriction.update(restriction)
        await self.security_manager.create_restriction([self.restriction])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.security_manager.remove_restriction([self.restriction['id']])
        await self.done({'result': 'deleted'})
