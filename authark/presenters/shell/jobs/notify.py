import json
import asyncio
from pathlib import Path
from typing import Dict, Optional
from aiohttp import ClientSession
from injectark import Injectark, Config
from schedulark import Task


class NotifyJob:
    def __init__(self, injector: Injectark) -> None:
        self.config = injector.config
        self.injector = injector
        self.session: Optional[ClientSession] = None

    async def __call__(self, task: Task) -> dict:
        self.session = self.session or ClientSession()

        payload = task.payload
        endpoint = self.config['notification']['url']
        async with self.session.patch(endpoint, json=payload) as response:
            pass

        return {}

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                return loop.create_task(self.session.close())
            loop.run_until_complete(self.session.close())
        except Exception:
            pass
