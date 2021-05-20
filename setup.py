#!/usr/bin/env python
import re
from textwrap import dedent

import setuptools

from where_was_i import __version__


def requires(prefix=''):
    """Retrieve requirements from requirements.txt
    """
    try:
        reqs = map(str.strip, open(prefix + 'requirements.txt').readlines())
        return [req for req in reqs if not re.match(r'\W', req)]
    except Exception:
        pass
    return []


setuptools.setup(
    name='where_was_i',
    version=__version__,
    install_requires=requires(),
    license='ASL 2.0',
    long_description=dedent("""\
        Parse Google's Semantic location into human-readable form

        Getting Started:
        ----------------
        To use where-was-i, install it in one of several ways.

          $ git clone https://github.com/lhh/where_was_i
          $ cd where_was_i
          $ pip install .
          $ where-was-i <args> *

        or by using pip:

          $ pip install where_was_i
          $ where-was-i <args>

        or by using the container build (does not support wildcards):

          $ git clone https://github.com/lhh/where_was_i
          $ cd where_was_i
          $ make
          $ ./where-was-i <args> < <filename>

        Examples:
         - where-was-i ~/2017/*
         - where-was-i -s -p ~/2017/2017_JANUARY.json
         - where-was-i < ~/2017/2017_JANUARY.json
        """),
    author='Lon Hohberger',
    author_email='lon@metamorphism.com',
    maintainer='Lon Hohberger',
    maintainer_email='lon@metamorphism.com',
    packages=['where_was_i'],
    url='http://github.com/lhh/where_was_i',
    data_files=[("", ["LICENSE"])],
    entry_points={'console_scripts': ['where-was-i = where_was_i.cli:main']},
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Natural Language :: English',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python',
                 'Topic :: Software Development',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Utilities'],
)
