#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from distutils.core import setup, Command
import django_data_mirror

setup(
    name='django-data-mirror',
    version=django_data_mirror.__version__,
    description='Allows caching remote API data in local Django models.',
    author='Chris Spencer',
    author_email='chrisspen@gmail.com',
    url='http://github.com/chrisspen/django-data-mirror',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    requires = ["Django (>=1.4)",],
#    cmdclass={
#        'test': TestCommand,
#    },
)