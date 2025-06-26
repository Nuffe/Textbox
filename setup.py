from setuptools import setup, find_packages

setup(
    name="textbox",
    version="0.1",
    packages=find_packages(),  # finds 'textbox/' package
    entry_points={
        "console_scripts": [
            "textbox=textbox.__main__:main",  # run `textbox` in shell
        ],
    },
)
