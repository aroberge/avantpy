def test_try_nobreak(capsys):
    from . import raise_try_nobreak

    if not hasattr(raise_try_nobreak, "err"):
        info = str(capsys.readouterr())
        raise_try_nobreak.err = info
    assert "TryNobreakError" in raise_try_nobreak.err


def test_try_nobreak2(capsys):
    from . import raise_try_nobreak2

    if not hasattr(raise_try_nobreak2, "err"):
        info = str(capsys.readouterr())
        raise_try_nobreak2.err = info
    assert "TryNobreakError" in raise_try_nobreak2.err
