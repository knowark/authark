from authark.application.informers import ComposingInformer


def test_composing_informer_methods():
    methods = ComposingInformer.__abstractmethods__  # type: ignore
    assert 'list_user_roles' in methods


async def test_composing_informer_list_user_roles(
        composing_informer: ComposingInformer) -> None:
    user_id = '1'
    result = await composing_informer.list_user_roles(user_id)
    assert isinstance(result, list)
    assert result[0] == {'ranking_id': '1', 'role': 'admin',
                         'dominion': 'Data Server'}
