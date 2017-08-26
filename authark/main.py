"""
Authark entrypoint.

Import 'app' to be run with gunicorn.
"""

from authark.infra.web.main import app
