def test_unknown_lang(capsys):
    from . import unknown_language

    if not hasattr(unknown_language, "out"):
        info = str(capsys.readouterr())
        unknown_language.out = info
    assert "UnknownLanguage" in unknown_language.out
