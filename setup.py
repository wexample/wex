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
)
