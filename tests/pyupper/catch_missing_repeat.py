def test_missing_repeat(capsys):
    from . import raise_missing_repeat

    if not hasattr(raise_missing_repeat, "err"):
        info = str(capsys.readouterr())
        raise_missing_repeat.err = info
    assert "MissingRepeatError" in raise_missing_repeat.err


def test_missing_repeat2(capsys):
    from . import raise_missing_repeat2

    if not hasattr(raise_missing_repeat2, "err"):
        info = str(capsys.readouterr())
        raise_missing_repeat2.err = info
    assert "MissingRepeatError" in raise_missing_repeat2.err
