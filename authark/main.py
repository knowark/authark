"""
Authark entrypoint.

Import 'app' to be run with gunicorn.
"""

from infra.web.main import app
