def test_missing_repeat_colon(capsys):
    from . import raise_missing_repeat_colon

    if not hasattr(raise_missing_repeat_colon, "err"):
        info = str(capsys.readouterr())
        raise_missing_repeat_colon.err = info
    assert "MissingRepeatColonError" in raise_missing_repeat_colon.err
