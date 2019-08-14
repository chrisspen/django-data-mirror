#!/usr/bin/env python
from optparse import make_option

# from django.conf import settings
from django.core.management.base import BaseCommand

from django_data_mirror.models import DataSource


class Command(BaseCommand):
    help = 'Attempts to generate Django models to store data from an external source.'
    args = '<target names>'
    option_list = BaseCommand.option_list + (
        make_option('--max-lines', dest='max_lines', default=1000, help='The maximum number of lines to look at from a feed.'),
    )

    def handle(self, *args, **options):
        target_names = set(_.strip() for _ in args)
        for cls in DataSource.__subclasses__():
            if cls.__name__ not in target_names:
                continue
            print(cls)
            cls.analyze(**options)
