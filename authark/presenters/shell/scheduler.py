import schedulark
from pathlib import Path
from injectark import Config, Injectark
from .jobs import JOBS


class Scheduler:
    def __init__(self, injector: Injectark) -> None:
        self.injector = injector
        self.config = injector.config
        self.session_manager = self.injector['SessionManager']

    async def run(self, options: dict) ->None:
        queue = schedulark.JsonQueue(str(Path.home() / 'data/tasks.json'))
        scheduler = schedulark.Scheduler(queue)

        for job in JOBS:
            scheduler.register(job(self.injector))

        if options.get('time'):
            return await scheduler.time()

        return await scheduler.work()
