from .development_config import DevelopmentConfig


class ProductionConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'PROD'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['database'] = {
            'type': 'json',
            'url': './authark_data.json'
        }

        # self.read_configuration_files()

    # def read_configuration_files(self):
    #     config_filename = '/config.json'
    #     paths = [
    #         '/etc/opt/authark' + config_filename,
    #         '/etc/authark' + config_filename,
    #         self['environment']['home'] + config_filename,
    #         '.' + config_filename
    #     ]
    #     for path in paths:
    #         config_dict = {}
    #         config_file = Path(path)
    #         if config_file.is_file():
    #             with config_file.open() as f:
    #                 try:
    #                     data = f.read()
    #                     config_dict = loads(data)
    #                 except JSONDecodeError:
    #                     pass
    #         self.update(config_dict)
