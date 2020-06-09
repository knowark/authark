from authark.core import json_setup_supplier, JsonSetupSupplier


def test_json_setup_supplier_setup(tmp_path):
    zones = {'default': str(tmp_path)}
    setup_supplier = JsonSetupSupplier(zones)
    setup_supplier.setup()
    assert (tmp_path / '__template__').exists()
