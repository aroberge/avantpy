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
    assert 'IfnobreakError' in if_nobreak.out


if __name__ == "__main__":
    test_if_nobreak()
    print("Success.")
