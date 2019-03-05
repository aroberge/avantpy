import pytest

def test_if_nobreak():
    with pytest.raises(SyntaxError):
        from . import if_nobreak

if __name__ == '__main__':
    test_if_nobreak()
    print("Success.")
