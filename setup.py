#pylint: skip-file
from setuptools import setup, find_packages
from distutils.util import convert_path

## converting readme for pypi
from pypandoc import convert
def convert_md(filename):
    return convert(filename, 'rst')

setup(name='avantpy',
    version='0.0.1',
    description="Python with training wheels: executable pseudocode in any language.",
    long_description = convert_md('README.md'),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Education',
        'Topic :: Education',
    ],
    url='https://github.com/aroberge/avantpy',
    author='André Roberge',
    author_email='Andre.Roberge@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['dist', 'build', 'tools']),
    zip_safe=False)
