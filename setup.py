from setuptools import setup, find_packages
from src.const.globals import WEX_VERSION

setup(
    name='wex',
    version=WEX_VERSION,
    description='A bash command manager',
    author='Wexample',
    author_email='contact@wexample.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wex = wex.__main__:main'
        ]
    },
    long_description="""Wex is a powerful command-line tool that allows you to manage your bash commands with ease. With Wex, you can easily create, organize, and execute bash commands from anywhere in your terminal.

    Features:
    - Manage your bash commands with ease
    - Create, organize, and execute bash commands from anywhere in your terminal
    - Simple and intuitive command-line interface

    Get started with Wex today and take control of your bash commands!"""
)
