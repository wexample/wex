from setuptools import setup, find_packages

setup(
    name='wex',
    version='5.0.0',
    description='A bash command manager',
    author='Wexample',
    author_email='contact@wexample.com',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
                         'console_scripts': [
                             'wex = myapp.index:main'
                         ]
                     },,
    classifiers=[
        'Development Status :: 5 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
