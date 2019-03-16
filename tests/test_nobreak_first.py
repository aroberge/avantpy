def test_if_nobreak2(capsys):
    from . import if_nobreak2

    if not hasattr(if_nobreak2, "out"):
        info = str(capsys.readouterr())
        if_nobreak2.out = info
    assert "NobreakFirstError" in if_nobreak2.out
