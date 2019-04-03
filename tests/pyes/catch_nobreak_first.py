def test_nobreak_first(capsys):
    from . import raise_nobreak_first

    if not hasattr(raise_nobreak_first, "err"):
        info = str(capsys.readouterr())
        raise_nobreak_first.err = info
    assert "NobreakFirstError" in raise_nobreak_first.err
