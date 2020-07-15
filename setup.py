from setuptools import setup

setup(
    name="FoxySheep",
    version="1.0.0",
    entry_points = {
        "console_scripts": [
            "foxy-sheep = FoxySheep.__main__:REPL",
            ]
            },
    install_requires=["antlr4-python3-runtime>=4.7,<4.8"]
)
