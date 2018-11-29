from .development_config import DevelopmentConfig


class TrialConfig(DevelopmentConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'TEST'
        self['gunicorn'].update({
            'debug': True
        })
