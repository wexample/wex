from setuptools import setup, find_packages
from src.helper.core import core_dir_get_version
import os

current_dir = os.path.dirname(__file__) + '/'


def read(file_name: str) -> str:
    return open(os.path.join(os.path.dirname(current_dir), file_name)).read()


with open('requirements.in') as f:
    requirements = f.read().splitlines()

setup(
    name='wex',
    version=core_dir_get_version(current_dir),
    description='A command manager',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Wexample',
    author_email='contact@wexample.com',
    url='https://github.com/wexample/wex',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=[
        'cli/wex-wrapper',
    ],
)
