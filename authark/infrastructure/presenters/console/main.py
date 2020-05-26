from widark import Application, Frame, Color
from injectark import Injectark
from ...core import Config


class ConsoleApplication(Application):
    def __init__(self, config: Config, injector: Injectark) -> None:
        self.config = config
        self.injector = injector
        super().__init__()

    async def build(self) -> None:
        self.menu = Frame(self, 'Menu').title_style(
            Color.PRIMARY()).style(border=[0])
        self.content = Frame(self, 'Content').title_style(
            Color.SUCCESS()).style(border=[0]).grid(col=1).weight(col=4)
