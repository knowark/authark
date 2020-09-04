import os
from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]


config = {
    "port": int(os.environ.get('AUTHARK_PORT', 6291)),
    "factory": os.environ.get('AUTHARK_FACTORY', 'JsonFactory'),
    "strategies": os.environ.get(
        'AUTHARK_STRATEGIES', 'base,crypto,json').split(','),

    "environment": {
        "home": "/opt/authark"
    },
    "tokens": {
        "tenant": {
            "algorithm": "HS256",
            "secret": os.environ.get('AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
            "lifetime": 86400
        },
        "access": {
            "algorithm": "HS256",
            "secret": os.environ.get('AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
            "lifetime": 86400
        },
        "refresh": {
            "algorithm": "HS256",
            "secret": os.environ.get('AUTHARK_TOKENS_SECRET', "DEVSECRET123"),
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

# DEVELOPMENT_CONFIG: Config = {**BASE, **{
# "mode": "DEV",
# "factory": "CheckFactory",
# "strategies": ["base", "check"]
# }}


# PRODUCTION_CONFIG: Config = {**BASE, **{
# "mode": "PROD",
# "factory": "JsonFactory",
# "strategies": ["base", "crypto", "json"],
# "zones": {
# "default": {
# "data": str(Path.home() / "data")
# }
# }
# }}
