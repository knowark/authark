from authark.core import TemplateSupplier, MemoryTemplateSupplier


def test_template_supplier_methods() -> None:
    methods = TemplateSupplier.__abstractmethods__  # type: ignore
    assert 'render' in methods


def test_template_supplier_render() -> None:
    template_supplier = MemoryTemplateSupplier()

    result = template_supplier.render('activation.html', {'token': 'ABC123'})

    assert result == "activation.html: {'token': 'ABC123'}"
