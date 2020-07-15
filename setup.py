from setuptools import setup

setup(
    name="FoxySheep",
    version="1.0.0",
    classifiers = [
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    ],
    entry_points={"console_scripts": ["foxy-sheep = FoxySheep.__main__:main",]},
    install_requires=["antlr4-python3-runtime>=4.7,<4.8", "click"],
)
