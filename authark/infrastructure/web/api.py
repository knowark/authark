from flask import Flask, got_request_exception, abort
import flask_restful
from ..resolver import Registry
from .resources import RootResource, UserResource, TokenResource
from .spec import create_spec


def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    print('?' * 300)
    print('SENDER::', sender)
    print('exception::', exception)
    print('extra::', extra)
    return abort(
        500, 'Course ||{}|| does not exist'.format(str(exception)))


class Api(flask_restful.Api):

    def handle_error(self, e):
        print('++++++++++++++++++++++++++++++++++++++++++++++')
        print("|"*100)

        print('============== ERROR|||||||||||||', e)

        return flask_restful.abort(
            500, message='Course ||{}|| does not exist'.format(str(e)))


def create_api(app: Flask, registry: Registry) -> None:

    # Restful API
    api = Api(app)
    spec = create_spec()
    registry['spec'] = spec

    got_request_exception.connect(log_exception, app)

    # Root Resource (Api Specification)
    api.add_resource(
        RootResource, '/', resource_class_kwargs=registry)

    # Tokens Resource
    path = "/tokens"
    api.add_resource(
        TokenResource,
        path, '/auth', '/login',
        resource_class_kwargs=registry)

    # Users Resource
    path = "/users"
    spec.path(path=path, resource=UserResource)
    api.add_resource(
        UserResource,
        path, '/register', '/signup',
        resource_class_kwargs=registry)
