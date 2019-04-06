def test_indentation1(capsys):
    from . import raise_indentation_error1

    if not hasattr(raise_indentation_error1, "err"):
        info = str(capsys.readouterr())
        raise_indentation_error1.err = info
    assert "IndentationError" in raise_indentation_error1.err


def test_indentation2(capsys):
    from . import raise_indentation_error2

    if not hasattr(raise_indentation_error2, "err"):
        info = str(capsys.readouterr())
        raise_indentation_error2.err = info
    assert "IndentationError" in raise_indentation_error2.err


def test_indentation3(capsys):
    from . import raise_indentation_error3

    if not hasattr(raise_indentation_error3, "err"):
        info = str(capsys.readouterr())
        raise_indentation_error3.err = info
    assert "IndentationError" in raise_indentation_error3.err
