def test_missingleftbracket(capsys):
    from . import raise_missing_left_bracket

    if not hasattr(raise_missing_left_bracket, "err"):
        info = str(capsys.readouterr())
        raise_missing_left_bracket.err = info
    assert "MissingLeftBracketError" in raise_missing_left_bracket.err
