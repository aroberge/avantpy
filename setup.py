# pylint: skip-file
from setuptools import setup, find_packages
from avantpy import version

version_ = version.__version__

with open("README.md", encoding="utf8") as f:
    README = f.read()

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
    install_requires=["friendly-traceback"],
    url="https://github.com/aroberge/avantpy",
    author="André Roberge",
    author_email="Andre.Roberge@gmail.com",
    packages=find_packages(exclude=["dist", "build", "tools"]),
    zip_safe=False,
)
