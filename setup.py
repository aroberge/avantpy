# pylint: skip-file
from setuptools import setup, find_packages
from distutils.util import convert_path

with open("README.md") as f:
    long_description_ = f.read()

with open("avantpy/version.py") as f:
    version_ = f.read().split("=")[-1].strip()[1:-1]

setup(
    name="avantpy",
    version=version_,
    description="Python with training wheels: executable pseudocode in any language.",
    long_description=long_description_,
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Education",
        "Topic :: Education",
    ],
    url="https://github.com/aroberge/avantpy",
    author="André Roberge",
    author_email="Andre.Roberge@gmail.com",
    license="MIT",
    packages=find_packages(exclude=["dist", "build", "tools"]),
    zip_safe=False,
)
