from widark import (
    Frame, Listbox, Label, Entry,
    Event, Modal, Button, Spacer, Color)


class PoliciesModal(Modal):
    def setup(self, **context) -> 'PoliciesModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.security_manager = self.injector['SecurityManager']
        self.role = context['role']
        self.policy = None
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None
        frame = Frame(
            self, title=f'Policies for role: {self.role["name"]}'
        ).title_style(Color.DANGER()).weight(4, 2)

        Button(frame, content='\U00002795 Create',
               command=self.on_create).grid(0, 0)
        Button(frame, content='\U00002716 Cancel',
               command=self.on_cancel).style(Color.WARNING()).grid(0, 1)
        Listbox(frame, data=['Resource', 'Privilege', 'Active'],
                orientation='horizontal').grid(1).span(col=3)

        self.body = Listbox(
            frame, command=self.on_body).grid(3).span(col=3).weight(9)

    async def on_modal_done(self, event: Event) -> None:
        self.remove(self.modal)
        self.modal = None
        await self.load()
        self.render()

    async def load(self) -> None:
        roles = await self.authark_informer.search(
            'policy', [('role_id', '=', self.role['id'])])
        self.body.setup(data=roles, fields=[
            'resource', 'privilege', 'active'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        self.policy = getattr(event.target.parent, 'item', None)
        if self.policy:
            self.modal = PolicyDetailsModal(
                self, injector=self.injector, policy=self.policy,
                done_command=self.on_modal_done,
                proportion={'height': 0.85, 'width': 0.90}).launch()

    async def on_create(self, event: Event) -> None:
        policy = {'id': '', 'resource': '', 'active': False, 'privilege': '',
                  'role_id': self.role['id']}
        self.modal = PolicyDetailsModal(
            self, injector=self.injector, policy=policy,
            done_command=self.on_modal_done,
            proportion={'height': 0.85, 'width': 0.90}).launch()

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})


class PolicyDetailsModal(Modal):
    def setup(self, **context) -> 'PolicyDetailsModal':
        self.injector = context['injector']
        self.security_manager = self.injector['SecurityManager']
        self.policy = context['policy']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        self.modal = None

        frame = Frame(
            self, title='Policy').title_style(Color.SUCCESS()).weight(4, 2)
        Label(frame, content='Resource:').grid(0, 0)
        self.resource = Entry(frame, content=self.policy['resource']).style(
            border=[0]).grid(0, 1).weight(col=2)
        Label(frame, content='Privilege:').grid(1, 0)
        self.privilege = Entry(frame, content=self.policy['privilege']).style(
            border=[0]).grid(1, 1).weight(col=2)
        Label(frame, content='Active:').grid(2, 0)
        self.active = Entry(frame, content=str(self.policy['active'])).style(
            border=[0]).grid(2, 1).weight(col=2)
        Label(frame, content='ID:').grid(3, 0)
        Label(frame, content=f'{self.policy["id"]}').grid(3, 1)

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
        policy = {
            'resource': self.resource.text,
            'active': bool(self.active.text.lower().replace('false', '')),
            'privilege': self.privilege.text.upper()
        }

        self.policy.update(policy)
        await self.security_manager.create_policy([self.policy])
        await self.done({'result': 'saved'})

    async def on_cancel(self, event: Event) -> None:
        await self.done({'result': 'cancelled'})

    async def on_delete(self, event: Event) -> None:
        await self.security_manager.remove_policy([self.policy['id']])
        await self.done({'result': 'deleted'})
