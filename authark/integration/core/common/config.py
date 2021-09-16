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
            'AUTHARK_SYSTEM_ID') or "11111111-1111-1111-1111-111111111111",
        "username": os.environ.get(
            'AUTHARK_SYSTEM_USERNAME') or "system",
        "tid": os.environ.get(
            'AUTHARK_SYSTEM_TID') or "11111111-1111-1111-1111-111111111111",
        "tenant": os.environ.get(
            'AUTHARK_SYSTEM_TENANT') or "system",
        "name": os.environ.get(
            'AUTHARK_SYSTEM_NAME') or "System User",
        "email": os.environ.get(
            'AUTHARK_SYSTEM_EMAIL') or "",
        "password": os.environ.get(
            'AUTHARK_SYSTEM_PASSWORD') or ""
    },
    "verification": {
        "url": os.environ.get('AUTHARK_VERIFICATION_URL') or "",
        "tempos_email": os.environ.get(
            'AUTHARK_VERIFICATION_TEMPOS_EMAIL') or "",
        "unsubscribe_link": os.environ.get(
            'AUTHARK_VERIFICATION_UNSUBSCRIBE_LINK') or "",
    },
    "tokens": {
        "rest": {
            "algorithm": "HS256",
            "secret": (os.environ.get('AUTHARK_TOKENS_SECRET') or
                       ""),
            "lifetime": 86400
        },
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
            Path.home() / "data/tenants.json")
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
    "scheduler": {
        "json": os.environ.get('AUTHARK_SCHEDULER_JSON_FILE') or str(
            Path.home() / "data/tasks.json")
    },
    "notification": {
        "url": os.environ.get('AUTHARK_NOTIFICATION_URL') or (
            "http://localhost"),
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
            },
            "facebook": {
                "client_id": os.environ.get(
                    'AUTHARK_FACEBOOK_CLIENT_ID') or "",
                "client_secret": os.environ.get(
                    'AUTHARK_FACEBOOK_CLIENT_SECRET') or "",
                "redirect_uri": os.environ.get(
                    'AUTHARK_FACEBOOK_REDIRECT_URI') or "",
            }
        }
    }
}


def sanitize(config):
    if type(config) is dict:
        return {key: sanitize(value) for key, value in
                config.items() if value and sanitize(value)}
    return config
