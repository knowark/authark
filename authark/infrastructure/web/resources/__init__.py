from .token import TokenResource
from .user import UserResource


from typing import Any, Dict, Tuple
from flask import request, render_template, make_response
from flask_restful import Resource


class RootResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.spec = kwargs.get('spec')

    def get(self) -> str:
        if 'api' in request.args:
            return self.spec.to_dict()

        template = render_template('index.html', url="/?api")
        response = make_response(template, 200, {
            'Content-Type': 'text/html'
        })

        return response
