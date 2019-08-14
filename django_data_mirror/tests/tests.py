"""
Quick run with:

    export TESTNAME=.testJobRawCommand; tox -e py27-django17

"""
from __future__ import print_function

# import os
# import sys
# import datetime
# from datetime import timedelta
# import time
# import socket
import warnings
# from multiprocessing import Process

# import pytz

# import six
# try:
# from io import StringIO
# from io import BytesIO
# except ImportError:
# from cStringIO import StringIO
# from cStringIO import StringIO as BytesIO

# import django
# from django.core.management import call_command
# from django.core import mail
from django.test import TestCase
# from django.test.client import Client
# from django.utils import timezone
# from django.contrib.auth.models import User
# from django.conf import settings
# from django.db.models import Max

# from chroniker.models import Job, Log
# from chroniker.admin import HTMLWidget
# # from chroniker.tests.commands import Sleeper, InfiniteWaiter, ErrorThrower
# # from chroniker.management.commands.cron import run_cron
# from chroniker import utils
# from chroniker import constants as c
# from chroniker import settings as _settings

warnings.simplefilter('error', RuntimeWarning)


class Tests(TestCase):

    fixtures = []

    def setUp(self):
        pass

    def test1(self):
        self.assertEqual(1, 1)
