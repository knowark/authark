import asyncio
import logging
from typing import Dict, Optional, Any
from aiohttp import ClientSession
from ...application.domain.common import NotificationError
from ...application.domain.services import NotificationService


class HttpNotificationService(NotificationService):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.endpoint = config['url']
        self.session: Optional[ClientSession] = None
        self.logger = logging.getLogger(__name__)

    async def notify(self, notification: Dict[str, Any]) -> None:
        self.session = self.session or ClientSession()
        payload = {'meta': {}, 'data': {
            'recipient': notification['recipient'],
            'context': notification
        }}
        self.logger.info(f'Sending {payload} to {self.endpoint}...')
        async with self.session.patch(self.endpoint, json=payload) as response:
            self.logger.info(f'Send response status: {response.status}.')

    def __del__(self):
        self.session and asyncio.run(self.session.close())
