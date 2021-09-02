from typing import Dict
from widark import (Frame, Listbox, Event, Modal, Label, Button, Color)


class CredentialsModal(Modal):
    def setup(self, **context) -> 'CredentialsModal':
        self.injector = context['injector']
        self.authark_informer = self.injector['StandardInformer']
        self.management_manager = self.injector['ManagementManager']
        self.user = context['user']
        return super().setup(**context) and self

    def build(self) -> None:
        super().build()
        frame = Frame(self, title='Credentials').title_style(
            Color.WARNING()).weight(4, 2)
        Listbox(frame, data=['ID', 'Type', 'Client', 'Value'],
                orientation='horizontal').grid(1).span(col=3)
        self.body = Listbox(frame).grid(3).span(col=3).weight(9)

    async def load(self) -> None:
        credentials = (await self.authark_informer.search({
            "meta": {
                "model": "credential",
                "domain": [('user_id', '=', self.user['id'])]
            }
        }))['data']
        self.body.setup(data=credentials, fields=[
            'id', 'type', 'client', 'value'], limit=10).connect()
