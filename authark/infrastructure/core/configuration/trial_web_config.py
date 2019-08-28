from .trial_config import TrialConfig


class TrialWebConfig(TrialConfig):
    def __init__(self):
        super().__init__()
        self['mode'] = 'TEST'
        self['gunicorn'].update({
            'debug': True
        })
        self['factory'] = 'WebFactory'
        self['strategy'].update({
            "JwtSupplier": {
                "method":  "jwt_supplier"
            },
            "Authenticate": {
                "method": "middleware_authenticate"
            }
        })
