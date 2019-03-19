# content of conftest.py
import pytest


def pytest_collect_file(parent, path):
    if path.ext.startswith(".py") and (
        path.basename.startswith("test_") or path.basename.startswith("catch_")
    ):
        return pytest.Module(path, parent)
