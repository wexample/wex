from setuptools import setup, find_packages
from src.const.globals import WEX_VERSION
import os


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='wex',
    version=WEX_VERSION,
    description='A bash command manager',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Wexample',
    author_email='contact@wexample.com',
    url='https://github.com/wexample/wex',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'wex = wex.__main__:main',
        ],
    },
)
