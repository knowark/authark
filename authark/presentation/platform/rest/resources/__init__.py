# from aiohttp import web
# from pathlib import Path
# from aiohttp_jinja2 import render_template
# from ..... import __version__
from .resource import Resource
#from .registration import RegistrationResource
from .tenant import TenantResource
from .root import RootResource
#from .verification import VerificationResource
#from .requisition import RequisitionResource


# class RootResource:
    # def __init__(self, spec) -> None:
        # self.spec = spec

    # async def get(self, request):
        # if 'api' in request.query:
            # return web.json_response(self.spec)

        # context = {'url': '/?api', 'version': __version__}
        # response = render_template('index.html', request, context)
        # response.headers['Content-Type'] = 'text/html'

        # return response
