# from pytest import fixture
# from authark.infrastructure.web import ServerApplication


# class MockApp:
#     pass


# @fixture
# def application():
#     options = {'reload': True}
#     return ServerApplication(MockApp(), options)


# def test_server_application_instantiation(application):
#     assert application is not None


# def test_server_application_load_config(application):
#     application.load_config()
#     assert application.cfg.reload is True


# def test_server_application_load(application):
#     result = application.load()
#     assert isinstance(result, MockApp)
