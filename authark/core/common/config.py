from typing import Dict, Any
from pathlib import Path


Config = Dict[str, Any]


BASE: Config = {
    "mode": "BASE",
    "environment": {
        "home": "/opt/authark"
    },
    "port": 6291,
    "tokens": {
        "tenant": {
            "algorithm": "HS256",
            "secret": "DEVSECRET123",
            "lifetime": 86400
        },
        "access": {
            "algorithm": "HS256",
            "secret": "DEVSECRET123",
            "lifetime": 86400
        },
        "refresh": {
            "algorithm": "HS256",
            "secret": "DEVSECRET123",
            "lifetime": 604800,
            "threshold": 86400
        }
    },
    "strategies": ["base"],
    "strategy": {},
    "tenancy": {
        "json": Path.home() / "tenants.json",
    },
    "zones": {
        "default": {
            "data": str(Path.home() / "data")
        }
    },
    "export": {
        "type": "json",
        "dir": Path.home() / "export"
    },
}

DEVELOPMENT_CONFIG: Config = {**BASE, **{
    "mode": "DEV",
    "factory": "CheckFactory",
    "strategies": ["base", "check"]
}}


PRODUCTION_CONFIG: Config = {**BASE, **{
    "mode": "PROD",
    "factory": "JsonFactory",
    "strategies": ["base", "crypto", "json"],
    "zones": {
        "default": {
            "data": str(Path.home() / "data")
        }
    }
}}
