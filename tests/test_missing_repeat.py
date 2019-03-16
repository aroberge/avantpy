def test_missing_repeat1(capsys):
    from . import until_no_repeat

    if not hasattr(until_no_repeat, "out"):
        info = str(capsys.readouterr())
        until_no_repeat.out = info
    assert "MissingRepeatError" in until_no_repeat.out


def test_missing_repeat2(capsys):
    from . import forever_no_repeat

    if not hasattr(forever_no_repeat, "out"):
        info = str(capsys.readouterr())
        forever_no_repeat.out = info
    assert "MissingRepeatError" in forever_no_repeat.out
