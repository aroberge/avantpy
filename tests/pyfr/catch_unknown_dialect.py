def test_unknown_dialect(capsys):
    from . import raise_unknown_dialect

    if not hasattr(raise_unknown_dialect, "out"):
        info = str(capsys.readouterr())
        raise_unknown_dialect.out = info
    assert "UnknownDialectError" in raise_unknown_dialect.out
