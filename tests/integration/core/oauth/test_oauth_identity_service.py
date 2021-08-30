import aiohttp
from pytest import fixture, raises
from authark.application.domain.services import IdentityService
from authark.integration.core.oauth import OauthIdentityService, PROVIDERS


class MockResponse:
    def __init__(self, data, status=200):
        self.data = data
        self.status = status

    async def json(self):
        return self.data


class MockSessionResponse:
    def __init__(self, data):
        self.response = MockResponse(data)

    async def __aenter__(self):
        return self.response

    async def __aexit__(self, type, exception, traceback):
        pass


class MockSession:
    post_response = MockSessionResponse({
        'access_token': 'ACCESS_TOKEN_1234'})
    get_response = MockSessionResponse({
        'email': 'jdoe@example.com', 'name': 'John Doe'})

    def post(self, endpoint, headers=None, data=None):
        self.post_endpoint = endpoint
        self.post_headers = headers
        self.post_data = data
        return self.post_response

    def get(self, endpoint, params=None):
        self.get_endpoint = endpoint
        self.get_params = params
        return self.get_response

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


async def xtest_oauth_identity_service_guarded_client_session(
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

    assert mock_session.post_endpoint == PROVIDERS[provider]['token_endpoint']
    assert mock_session.post_headers == {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    assert mock_session.post_data == (
        'client_id=client_id_abcd1234&client_secret=TOP_SECRET'
        '&redirect_uri=https%3A%2F%2Fdash.proser.com%2Flogin'
        '&grant_type=authorization_code&code=ABCD_1234'
    )

    assert mock_session.get_endpoint == PROVIDERS[provider]['info_endpoint']
    assert mock_session.get_params == {'access_token': 'ACCESS_TOKEN_1234'}


async def test_oauth_identity_without_access_token(oauth_identity_service):
    mock_session = MockSession()
    oauth_identity_service.session = mock_session

    mock_session.post_response.response.data = {'error': 'access denied'}

    provider = 'google'
    code = 'ABCD_1234'
    with raises(ValueError):
        await oauth_identity_service.identify(provider, code)
