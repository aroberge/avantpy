# pylint: skip-file
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

with open("avantpy/version.py") as f:
    version_ = f.read().split("=")[-1].strip()[1:-1]

setup(
    name="avantpy",
    version=version_,
    description="Python with training wheels: executable pseudocode in any language.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Education",
        "Topic :: Education",
    ],
    url="https://github.com/aroberge/avantpy",
    author="André Roberge",
    author_email="Andre.Roberge@gmail.com",
    packages=find_packages(exclude=["dist", "build", "tools"]),
    zip_safe=False,
)
