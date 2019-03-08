from .token import TokenResource
from .user import UserResource

from typing import Any, Dict, Tuple
from flask import request, render_template, make_response, jsonify
from flask.views import MethodView


class RootResource(MethodView):

    def __init__(self, registry) -> None:
        self.spec = registry.get('spec')

    def get(self) -> str:
        print('REQUEST::::', request, request.args)

        if 'api' in request.args:
            return jsonify(self.spec.to_dict())

        template = render_template('index.html', url="/?api")
        response = make_response(template, 200, {
            'Content-Type': 'text/html'
        })

        return response
