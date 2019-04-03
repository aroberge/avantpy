def test_name_error(capsys):
    from . import raise_name_error

    if not hasattr(raise_name_error, "err"):
        info = str(capsys.readouterr())
        raise_name_error.err = info
    assert "NameError" in raise_name_error.err
