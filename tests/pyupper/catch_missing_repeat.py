def test_missing_repeat(capsys):
    from . import raise_missing_repeat

    if not hasattr(raise_missing_repeat, "out"):
        info = str(capsys.readouterr())
        raise_missing_repeat.out = info
    assert "MissingRepeatError" in raise_missing_repeat.out


def test_missing_repeat2(capsys):
    from . import raise_missing_repeat2

    if not hasattr(raise_missing_repeat2, "out"):
        info = str(capsys.readouterr())
        raise_missing_repeat2.out = info
    assert "MissingRepeatError" in raise_missing_repeat2.out
