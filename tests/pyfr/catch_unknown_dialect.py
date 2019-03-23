def test_unknown_dialect(capsys):
    from . import raise_unknown_dialect

    if not hasattr(raise_unknown_dialect, "err"):
        info = str(capsys.readouterr())
        raise_unknown_dialect.err = info
    assert "UnknownDialectError" in raise_unknown_dialect.err
