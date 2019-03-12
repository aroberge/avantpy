
def test_nobreak_else(capsys):
    from . import nobreak_else 
    if not hasattr(nobreak_else, "out"):
        info = str(capsys.readouterr())
        nobreak_else.out = info
    assert 'TrynobreakError' in nobreak_else.out
