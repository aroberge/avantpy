# content of conftest.py
import pytest

def pytest_collect_file(parent, path):
    if path.ext.startswith(".py") and path.basename.startswith("test"):
        return pytest.Module(path, parent)
