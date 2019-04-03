def test_nobreak_syntax(capsys):
    from . import raise_nobreak_syntax

    if not hasattr(raise_nobreak_syntax, "err"):
        info = str(capsys.readouterr())
        raise_nobreak_syntax.err = info
    assert "NobreakSyntaxError" in raise_nobreak_syntax.err


def test_nobreak_syntax2(capsys):
    from . import raise_nobreak_syntax2

    if not hasattr(raise_nobreak_syntax2, "err"):
        info = str(capsys.readouterr())
        raise_nobreak_syntax2.err = info
    assert "NobreakSyntaxError" in raise_nobreak_syntax2.err
