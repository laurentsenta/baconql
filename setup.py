from __future__ import print_function

import sys
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

try:
    import pypandoc

    description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    print("Missing pandoc module to build the README.", file=sys.stderr)
    description = ''

with open(path.join(here, 'baconql', 'VERSION'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
        name='baconql',
        version=version,
        description='Python SQL without ORM & easy migrations',
        long_description=description,

        url='https://github.com/lsenta/baconql',
        author='lsenta',
        # author_email='',
        # maintainer='',
        # maintainer_email='',

        # license='',

        packages=find_packages(),
        package_dir={'baconql.test': 'test'},
        include_package_data=True,

        entry_points={
            'console_scripts': ['baconql = baconql.cli:execute']
        },
        classifiers=[
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Developers',

            # TODO: Add Topic :: etc
            # TODO: Add License :: etc

            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
        ],
        install_requires=[
            'SQLAlchemy>=1.0',
            'click>=6.6',
            'Jinja2>=2.8',
            'sqlparse>=0.1'
        ]
)
