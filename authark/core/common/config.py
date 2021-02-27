import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]


config = {
    "port": int(os.environ.get('AUTHARK_PORT', 6291)),
    "factory": os.environ.get('AUTHARK_FACTORY', 'WebFactory'),
    "environment": {
        "home": "/opt/authark"
    },
    "system": {
        "id": os.environ.get(
            'AUTHARK_SYSTEM_ID',
            "3180ba1e-db99-499f-82c0-a881f55fd636"),
        "username": os.environ.get(
            'AUTHARK_SYSTEM_USERNAME', "system"),
        "name": os.environ.get(
            'AUTHARK_SYSTEM_NAME', "System User"),
        "email": os.environ.get(
            'AUTHARK_SYSTEM_EMAIL', ""),
        "password": os.environ.get(
            'AUTHARK_SYSTEM_PASSWORD', "")
    },
    "mail": {
        "sender": os.environ.get(
            'AUTHARK_MAIL_SENDER', ""),
        "host": os.environ.get(
            'AUTHARK_MAIL_HOST', ""),
        "port": int(os.environ.get(
            'AUTHARK_MAIL_PORT', 0)),
        "username": os.environ.get(
            'AUTHARK_MAIL_USERNAME', ""),
        "password": os.environ.get(
            'AUTHARK_MAIL_PASSWORD', "")
    },
    "tokens": {
        "tenant": {
            "algorithm": "HS256",
            "secret": os.environ.get(
                'AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
            "lifetime": 86400
        },
        "access": {
            "algorithm": "HS256",
            "secret": os.environ.get(
                'AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
            "lifetime": 86400
        },
        "refresh": {
            "algorithm": "HS256",
            "secret": os.environ.get(
                'AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
            "lifetime": 604800,
            "threshold": 86400
        }
    },
    "tenancy": {
        "json": os.environ.get('AUTHARK_TENANCY_JSON',
                               str(Path.home() / "tenants.json"))
    },
    "zones": {
        "default": {
            "data": os.environ.get('AUTHARK_ZONES_DEFAULT_DATA',
                                   str(Path.home() / "data"))
        }
    },
    "export": {
        "type": "json",
        "dir": os.environ.get('AUTHARK_EXPORT_DIR',
                              str(Path.home() / "export"))
    }
}


def sanitize(config):
    if type(config) is dict:
        return {key: sanitize(value) for key, value in
                config.items() if value and sanitize(value)}
    return config
