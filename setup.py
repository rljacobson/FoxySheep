from distutils.core import setup
import os.path as osp
from setuptools import find_packages


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


srcdir = get_srcdir()


def read(*rnames):
    return open(osp.join(srcdir, *rnames)).read()


long_description = read("README.rst") + "\n"
exec(read("FoxySheep/version.py"))

setup(
    name="FoxySheep",
    author="Robert Jacobson",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    description="Mathematica parser and translator",
    version=VERSION,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["foxy-sheep = FoxySheep.__main__:main"]},
    install_requires=["antlr4-python3-runtime>=4.7,<4.8", "click >= 7.1.2", "astor", "PyYAML", "astpretty"],
    url="http://github.com/rocky/FoxySheep2",
)
