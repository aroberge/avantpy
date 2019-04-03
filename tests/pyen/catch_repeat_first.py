def test_repeat_first(capsys):
    from . import raise_repeat_first

    if not hasattr(raise_repeat_first, "err"):
        info = str(capsys.readouterr())
        raise_repeat_first.err = info
    assert "RepeatFirstError" in raise_repeat_first.err
