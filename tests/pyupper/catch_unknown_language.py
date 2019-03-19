def test_unknown_lang(capsys):
    from . import raise_unknown_language

    if not hasattr(raise_unknown_language, "out"):
        info = str(capsys.readouterr())
        raise_unknown_language.out = info
    assert "UnknownLanguageError" in raise_unknown_language.out
