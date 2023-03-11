from setuptools import setup, find_packages

setup(
    name='wex',
    version='5.0.0',
    description='A bash command manager',
    author='Wexample',
    author_email='contact@wexample.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wex = myapp.index:main'
        ]
    },
)
