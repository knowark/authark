
def test_setup_manager(setup_manager):
    assert hasattr(setup_manager, 'setup')


async def test_setup_manager_setup(
    setup_manager, setup_supplier):
    result = await setup_manager.setup({})
    assert result == {}
