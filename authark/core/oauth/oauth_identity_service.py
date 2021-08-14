import asyncio
import base64
# import jwt
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
        parameters = { **PROVIDERS[provider]['token_parameters'],
                      **self.config['providers'][provider] }
        parameters['code'] = code

        endpoint = PROVIDERS[provider]['token_endpoint']
        headers: dict = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
        data = urlencode(parameters)
        async with self.session.post(
            endpoint, headers=headers, data=data) as response:
            access_token = (await response.json()).get('access_token')
            if not access_token:
                raise ValueError(f"Couldn't identify user through {provider}")

        info_endpoint = PROVIDERS[provider]['info_endpoint']
        parameters = {**PROVIDERS[provider]['info_parameters'],
                      'access_token': access_token}

        async with self.session.get(
            info_endpoint, params=parameters) as response:
            info = await response.json()

        return  User(email=info['email'], name=info['name'])

    def __del__(self):
        self.session and asyncio.run(self.session.close())


PROVIDERS: Dict[str, Any] = {
    'google': {
        'token_endpoint': (
            'https://oauth2.googleapis.com/token'),
        'token_parameters': {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'grant_type': 'authorization_code',
        },
        'info_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo',
        'info_parameters': {},
    },
    'facebook': {
        'token_endpoint': (
            'https://graph.facebook.com/v11.0/oauth/access_token'),
        'token_parameters': {
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'grant_type': 'authorization_code',
        },
        'info_endpoint': 'https://graph.facebook.com/me',
        'info_parameters': {
            'fields': 'name,email'
        },
    }
}
