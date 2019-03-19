def test_try_nobreak(capsys):
    from . import raise_try_nobreak

    if not hasattr(raise_try_nobreak, "out"):
        info = str(capsys.readouterr())
        raise_try_nobreak.out = info
    assert "TryNobreakError" in raise_try_nobreak.out


def test_try_nobreak2(capsys):
    from . import raise_try_nobreak2

    if not hasattr(raise_try_nobreak2, "out"):
        info = str(capsys.readouterr())
        raise_try_nobreak2.out = info
    assert "TryNobreakError" in raise_try_nobreak2.out
