import asyncio
from urllib.parse import urlencode
from aiohttp import ClientSession
from typing import Dict, Optional, Any
from ...application.domain.models import User
from ...application.domain.services import IdentityService


class OauthIdentityService(IdentityService):
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.session: Optional[ClientSession] = None

    async def identify(self, provider: str, code: str) -> User:
        self.session = self.session or ClientSession()
        parameters = { **PROVIDERS[provider]['tokenParameters'],
                      **self.config['providers'][provider] }

        endpoint = PROVIDERS[provider]['tokenEndpoint']
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        data = urlencode(parameters)
        async with self.session.post(
            endpoint, headers=headers, data=data) as response:
            result = await response.json()

        user =  User(email='any')
        return user

    def __del__(self):
        self.session and asyncio.run(self.session.close())


PROVIDERS: Dict[str, Any] = {
    'google': {
        'tokenEndpoint': 'https://oauth2.googleapis.com/token',
        'tokenParameters': {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'grant_type': 'authorization_code',
        }
    },
    'facebook': {
        'tokenEndpoint': 'https://graph.facebook.com/v11.0/oauth/access_token',
        'tokenParameters': {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'grant_type': 'authorization_code',
        }
    }
}
