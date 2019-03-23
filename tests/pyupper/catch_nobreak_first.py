def test_if_nobreak2(capsys):
    from . import raise_nobreak_first

    if not hasattr(raise_nobreak_first, "err"):
        info = str(capsys.readouterr())
        raise_nobreak_first.err = info
    assert "NobreakFirstError" in raise_nobreak_first.err
