from authark.infrastructure.config.context import Context
from authark.infrastructure.terminal.panel import Panel


def create_panel(context: Context) -> Panel:
    main = Panel(context)
    return main
