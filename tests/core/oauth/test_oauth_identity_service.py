import aiohttp
from pytest import fixture
from authark.application.domain.services import IdentityService
from authark.core.oauth import OauthIdentityService, PROVIDERS


class MockResponse:
    status = 200
    async def json(self):
        return {}
        print('response')


class MockSessionResponse:
    response = MockResponse()
    async def __aenter__(self):
        return self.response

    async def __aexit__(self, type, exception, traceback):
        pass


class MockSession:
    session_response = MockSessionResponse()
    def post(self, endpoint, headers=None, data=None):
        self.endpoint = endpoint
        self.headers = headers
        self.data = data
        return self.session_response

    async def close(self):
        pass


@fixture
async def oauth_identity_service():
    config = {
        "providers": {
            "google": {
                "client_id": "client_id_abcd1234",
                "client_secret": "TOP_SECRET",
                "redirect_uri": "https://dash.proser.com/login",
            }
        }
    }
    identity_service = OauthIdentityService(config)
    return identity_service


async def test_oauth_identity_service_instantiation(oauth_identity_service):
    assert isinstance(oauth_identity_service, IdentityService)


async def test_oauth_identity_service_guarded_client_session(
    oauth_identity_service):

    provider = 'google'
    code = 'ABCD_1234'
    user = await oauth_identity_service.identify(provider, code)

    assert isinstance(oauth_identity_service.session, aiohttp.ClientSession)


async def test_oauth_identity_service_identify(oauth_identity_service):
    mock_session = MockSession()
    oauth_identity_service.session = mock_session

    provider = 'google'
    code = 'ABCD_1234'
    user = await oauth_identity_service.identify(provider, code)

    assert mock_session.endpoint == PROVIDERS[provider]['tokenEndpoint']
    assert mock_session.headers == {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    assert mock_session.data == (
        'client_id=client_id_abcd1234&client_secret=TOP_SECRET'
        '&redirect_uri=https%3A%2F%2Fdash.proser.com%2Flogin'
        '&grant_type=authorization_code'
    )
