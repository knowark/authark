import pathlib
import aiohttp

bind = '0.0.0.0:8000'
workers = 1

worker_class = "aiohttp.GunicornWebWorker"
chdir = (
    str(pathlib.Path.home()) + "/Workspace/dev/git.nubark.com/"
    "nubark-apps/authark/authark"
)
