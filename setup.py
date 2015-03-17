#!/usr/bin/env python
"""
    Norman Messtorff <normes@normes.org>
    (c) 2014 - 2015
"""
import io
import os
from setuptools import setup, find_packages
import keynoteapi

PKG_VER = keynoteapi.__version__


def read(*filenames, **kwargs):
    """
        Read files and join them for a long description.
    """
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        if os.path.isfile(filename):
            with io.open(filename, encoding=encoding) as filesocket:
                buf.append(filesocket.read())
    return sep.join(buf)

setup(
    name='keynoteapi',
    packages=find_packages(exclude=['tests']),
    description='Access the Keynote Systems API (api.keynote.com)',
    long_description=read('README.md'),
    version=PKG_VER,
    url='http://github.com/nmesstorff/keynoteapi/',
    download_url="http://github.com/nmesstorff/keynoteapi/tarball/v" + PKG_VER,
    license='Apache Software License',
    author='Norman Messtorff',
    author_email='normes@normes.org',

    platforms='any',
    install_requires=read('requirements.txt'),
    setup_requires=['nose >= 1.0', 'coverage', 'pylint', 'pep8'],
    test_suite='nose.collector',

    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    keywords=['keynote', 'systems', 'keynote systems', 'monitoring',
              'perfomance', 'metric', 'dashboarddata']
)
