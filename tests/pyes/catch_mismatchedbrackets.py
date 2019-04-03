def test_mismatchedbrackets(capsys):
    from . import raise_mismatched_brackets

    if not hasattr(raise_mismatched_brackets, "err"):
        info = str(capsys.readouterr())
        raise_mismatched_brackets.err = info
    assert "MismatchedBracketsError" in raise_mismatched_brackets.err
