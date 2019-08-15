#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

import django_data_mirror

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_reqs(*fns):
    lst = []
    for fn in fns:
        for package in open(os.path.join(CURRENT_DIR, fn)).readlines():
            package = package.strip()
            if not package:
                continue
            lst.append(package.strip())
    return lst


setup(
    name='django-data-mirror',
    version=django_data_mirror.__version__,
    packages=find_packages(),
    description='Allows caching remote API data in local Django models.',
    author='Chris Spencer',
    license="LGPLv3",
    author_email='chrisspen@gmail.com',
    url='http://github.com/chrisspen/django-data-mirror',
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    install_requires=get_reqs('requirements.txt', 'requirements-django.txt'),
    tests_require=get_reqs('requirements-test.txt'),
)
