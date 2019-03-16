def test_unknown_dialect(capsys):
    from . import unknown_dialect

    if not hasattr(unknown_dialect, "out"):
        info = str(capsys.readouterr())
        unknown_dialect.out = info
    assert "UnknownDialect" in unknown_dialect.out
