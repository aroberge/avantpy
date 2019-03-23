def test_if_nobreak(capsys):
    from . import raise_if_nobreak

    if not hasattr(raise_if_nobreak, "err"):
        info = str(capsys.readouterr())
        raise_if_nobreak.err = info
    assert "IfNobreakError" in raise_if_nobreak.err
