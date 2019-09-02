# -*- coding: utf-8 -*-
import os
from aliaxer import aliaxer

long_description = aliaxer.read('README.txt')

setup(
    name='aliaxer',
    version=aliaxer.__version__,
    url='https://github.com/moijafcor/Aliaxer',
    license='GNU General Public License Version 3',
    author='Moises Jafet Cornelio',
    tests_require=[],
    install_requires=[],
    cmdclass={},
    author_email='cv at moisesjafet dot com',
    description='Basic alias manager for the Terminal warrior.',
    long_description=long_description,
    packages=['aliaxer'],
    include_package_data=True,
    platforms='any',
    test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: Stable',
        'Natural Language :: English',
        'Environment :: Terminal',
        'Intended Audience :: Developers, SysAdmins and DevOps',
        'License :: GNU General Public License Version 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Utilities',
        'Topic :: System Administration :: Utilities',
        ],
    extras_require={
        'testing': [],
    }
)
