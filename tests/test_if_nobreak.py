def test_if_nobreak(capsys):
    from . import if_nobreak

    # if_nobreak raises an error which will result in a
    # print statement; it is printed out when pytest
    # collects the tests.
    # After collecting the test, they are run and
    # no print statement will be done from the import
    # This is why we cache it so that we can see it
    # both times.
    if not hasattr(if_nobreak, "out"):
        info = str(capsys.readouterr())
        if_nobreak.out = info
    assert "IfNobreakError" in if_nobreak.out


def test_if_nobreak3(capsys):
    from . import ifnobreakerror

    if not hasattr(ifnobreakerror, "out"):
        info = str(capsys.readouterr())
        ifnobreakerror.out = info
    assert "IfNobreakError" in ifnobreakerror.out
