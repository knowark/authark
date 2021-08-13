from authark.application.general import (
    IdentitySupplier, MemoryIdentitySupplier)


def test_identity_supplier_methods() -> None:
    methods = IdentitySupplier.__abstractmethods__  # type: ignore
    assert 'identify' in methods


def test_memory_identity_supplier_instantiation() -> None:
    identity_supplier = MemoryIdentitySupplier()

    assert isinstance(identity_supplier, IdentitySupplier)


async def test_memory_identity_supplier_identify() -> None:
    identity_supplier = MemoryIdentitySupplier()

    user = await identity_supplier.identify('famunoz@knowark.com', 'secret1234')
    assert isinstance(identity_supplier, IdentitySupplier)
