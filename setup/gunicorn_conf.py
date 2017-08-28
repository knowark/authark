import pathlib


bind = '0.0.0.0:8000'
workers = 1

worker_class = "gevent"
chdir = (
    str(pathlib.Path.home()) + "/Workspace/dev/git.nubark.com/"
    "nubark-apps/authark/authark"
)
