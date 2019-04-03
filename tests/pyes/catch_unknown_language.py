def test_unknown_lang(capsys):
    from . import raise_unknown_language

    if not hasattr(raise_unknown_language, "err"):
        info = str(capsys.readouterr())
        raise_unknown_language.err = info
    assert "UnknownLanguageError" in raise_unknown_language.err
