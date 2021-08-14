import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]


config = {
    "port": int(os.environ.get('AUTHARK_PORT') or 6291),
    "factory": os.environ.get('AUTHARK_FACTORY') or 'OauthFactory',
    "templates": (os.environ.get('AUTHARK_TEMPLATES') or ".").split(','),
    "environment": {
        "home": "/opt/authark"
    },
    "system": {
        "id": os.environ.get(
            'AUTHARK_SYSTEM_ID') or "3180ba1e-db99-499f-82c0-a881f55fd636",
        "username": os.environ.get(
            'AUTHARK_SYSTEM_USERNAME') or "system",
        "name": os.environ.get(
            'AUTHARK_SYSTEM_NAME') or "System User",
        "email": os.environ.get(
            'AUTHARK_SYSTEM_EMAIL') or "",
        "password": os.environ.get(
            'AUTHARK_SYSTEM_PASSWORD') or ""
    },
    "verification": {
        "url": os.environ.get('AUTHARK_VERIFICATION_URL') or "",
    },
    "mail": {
        "sender": os.environ.get('AUTHARK_MAIL_SENDER') or "",
        "host": os.environ.get('AUTHARK_MAIL_HOST') or "",
        "port": int(os.environ.get('AUTHARK_MAIL_PORT') or 0),
        "username": os.environ.get('AUTHARK_MAIL_USERNAME') or "",
        "password": os.environ.get('AUTHARK_MAIL_PASSWORD') or ""
    },
    "tokens": {
        "tenant": {
            "algorithm": "HS256",
            "secret": (os.environ.get('AUTHARK_TOKENS_SECRET') or
                       "DEVSECRET123"),
            "lifetime": 86400
        },
        "access": {
            "algorithm": "HS256",
            "secret": (os.environ.get('AUTHARK_TOKENS_SECRET') or
                       "DEVSECRET123"),
            "lifetime": 86400
        },
        "verification": {
            "algorithm": "HS256",
            "secret": (os.environ.get('AUTHARK_TOKENS_SECRET') or
                       "DEVSECRET123"),
            "lifetime": 86400
        },
        "refresh": {
            "algorithm": "HS256",
            "secret": (os.environ.get('AUTHARK_TOKENS_SECRET') or
                       "DEVSECRET123"),
            "lifetime": 604800,
            "threshold": 86400
        }
    },
    "tenancy": {
        "json": os.environ.get('AUTHARK_TENANCY_JSON') or str(
            Path.home() / "tenants.json")
    },
    "zones": {
        "default": {
            "data": os.environ.get('AUTHARK_ZONES_DEFAULT_DATA') or str(
                Path.home() / "data")
        }
    },
    "export": {
        "type": "json",
        "dir": os.environ.get('AUTHARK_EXPORT_DIR') or str(
            Path.home() / "export")
    },
    "oauth": {
        "providers": {
            "google": {
                "client_id": os.environ.get(
                    'AUTHARK_GOOGLE_CLIENT_ID') or "",
                "client_secret": os.environ.get(
                    'AUTHARK_GOOGLE_CLIENT_SECRET') or "",
                "redirect_uri": os.environ.get(
                    'AUTHARK_GOOGLE_REDIRECT_URI') or "",
            }
        }
    }
}


def sanitize(config):
    if type(config) is dict:
        return {key: sanitize(value) for key, value in
                config.items() if value and sanitize(value)}
    return config
