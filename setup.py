#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import microbus

setup(
    name='microbus',
    version=microbus.__version__,
    url='http://github.com/tgalal/microbus',
    license='MIT',
    author='Tarek Galal',
    tests_require=[],
    install_requires = ["zyklus"],
    author_email='tare2.galal@gmail.com',
    description=' A simple detached data carrying mechanism across different stages of a pipeline design or similar ',
    #long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    # test_suite='',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        #'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
