def test_tab_error(capsys):
    from . import raise_tab_error

    if not hasattr(raise_tab_error, "err"):
        info = str(capsys.readouterr())
        raise_tab_error.err = info
    assert "TabError" in raise_tab_error.err
