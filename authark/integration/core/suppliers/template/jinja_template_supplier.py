from typing import Dict, Any
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .template_supplier import TemplateSupplier


class JinjaTemplateSupplier(TemplateSupplier):
    def __init__(self, paths = []) -> None:
        core_directory = Path(__file__).parent.parent.parent
        core_templates = str(core_directory / 'templates')
        template_paths = paths + [core_templates]

        self.env = Environment(
            loader=FileSystemLoader(template_paths, followlinks=True),
            autoescape=select_autoescape(['html', 'xml']))

    def render(self, template: str, context: Dict[str, Any]):
        return self.env.get_template(template).render(**context)
