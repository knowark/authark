from authark.application.operation.informers import ComposingInformer


async def test_composing_informer_list_user_roles(
        composing_informer: ComposingInformer) -> None:
    user_id = '1'
    result = (await composing_informer.list_user_roles({
        "data":user_id
        }))['data']
    assert isinstance(result, list)
    assert result[0] == {'ranking_id': '1', 'role': 'admin',
                         'dominion': 'Data Server'}
