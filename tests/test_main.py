from authark.__main__ import main


def test_main_definition():
    """
    Only assert if the function is defined.
    The function is not tested as it serves
    just as a bootstrapping mechanism for
    the application.
    """
    assert main is not None
