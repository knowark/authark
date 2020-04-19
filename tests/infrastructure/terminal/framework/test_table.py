# import urwid
# from authark.infrastructure.terminal.framework.table import Table


# def test_table_instantiation(table):
#     assert table is not None


# def test_table_build_header(table):
#     headers_list = ['name', 'age', 'height']
#     result = table._build_header(headers_list)
#     rendered_result = result.render((40,)).text
#     assert result is not None
#     assert len(rendered_result) == 2
#     assert b'NAME'in rendered_result[0]


# def test_table_keypress(table):
#     table.keypress(None, 'home')
#     home_focused_widget = table._w.focus.render((40,)).text
#     assert b'Esteban' in home_focused_widget[0]
#     table.keypress(None, 'end')
#     end_focused_widget = table._w.focus.render((40,)).text
#     assert b'Cesar' in end_focused_widget[0]
#     table.keypress(None, 'up')
#     up_focused_widget = table._w.focus.render((40,)).text
#     assert b'Adriana' in up_focused_widget[0]
#     table.keypress(None, 'down')
#     down_focused_widget = table._w.focus.render((40,)).text
#     assert b'Cesar' in down_focused_widget[0]


# def test_table_get_selected_item(table):
#     result = table.get_selected_item()
#     assert result == {'age': 29, 'name': 'Esteban'}
#     table.keypress(None, 'down')
#     result = table.get_selected_item()
#     assert result['name'] == 'Adriana'
