#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Command

import django_data_mirror

setup(
    name='django-data-mirror',
    version=django_data_mirror.__version__,
    packages = find_packages(),
    description='Allows caching remote API data in local Django models.',
    author='Chris Spencer',
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
    requires = ["Django (>=1.4)",],
#    cmdclass={
#        'test': TestCommand,
#    },
)