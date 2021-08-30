from authark.integration.core import (
    TemplateSupplier, MemoryTemplateSupplier, JinjaTemplateSupplier)


def test_template_supplier_methods() -> None:
    methods = TemplateSupplier.__abstractmethods__  # type: ignore
    assert 'render' in methods


def test_template_supplier_render() -> None:
    template_supplier = MemoryTemplateSupplier()

    result = template_supplier.render('activation.html', {'token': 'ABC123'})

    assert result == "activation.html: {'token': 'ABC123'}"

def test_jinja_template_supplier_render(tmp_path) -> None:
    templates_dir = tmp_path / 'templates'
    templates_dir.mkdir()
    custom_template = templates_dir / 'custom.html'
    custom_template.write_text(
"""<!DOCTYPE html>
<html>
  <head>
      <title>{{ site }}</title>
  </head>
  <body>
    <h1>Hello</h1>
    <p>{{ username }}</p>
  </body>
</html>""")

    template_supplier = JinjaTemplateSupplier([templates_dir])

    result = template_supplier.render('custom.html', {
        'site': 'Knowark',
        'username': 'grinberg'
    })

    assert result == (
"""<!DOCTYPE html>
<html>
  <head>
      <title>Knowark</title>
  </head>
  <body>
    <h1>Hello</h1>
    <p>grinberg</p>
  </body>
</html>""")
