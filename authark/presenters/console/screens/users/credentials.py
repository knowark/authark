from typing import Dict
from widark import (Frame, Listbox, Event, Modal, Label, Button, Color)


class CredentialsModal(Modal):
    def setup(self, **context) -> 'CredentialsModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['AutharkInformer']
        self.management_manager = self.injector['ManagementManager']
        self.user = context['user']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        frame = Frame(self, title='Credentials').title_style(
            Color.WARNING()).weight(4, 2)
        Listbox(frame, data=['ID', 'Type', 'Client', 'Value'],
                orientation='horizontal').grid(1).span(col=3)
        self.body = Listbox(frame, command=self.on_body).grid(
            3).span(col=3).weight(9)

    async def load(self) -> None:
        credentials = await self.authark_informer.search(
            'credential', [('user_id', '=', self.user['id'])])
        self.body.setup(data=credentials, fields=[
            'id', 'type', 'client', 'value'], limit=10).connect()

    async def on_body(self, event: Event) -> None:
        credential = getattr(event.target.parent, 'item', None)
