#!/usr/bin/env python
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from django_data_mirror.models import DataSource

class Command(BaseCommand):
    help = 'Updated models storing data from an external source.'
    args = '<target names>'
    option_list = BaseCommand.option_list + (
        make_option('--bulk',
            dest='bulk',
            action='store_true',
            default=False,
            help='If given, attempts to download bulk data instead of incrementally.'),
        make_option('--fn',
            dest='fn',
            help='If given, the local filename to use.'),
        make_option('--skip-to',
            dest='skip_to',
            help='A record indicator that the backend processor should start from.'),
        make_option('--no-download',
            dest='no_download',
            action='store_true',
            default=False,
            help='If given, no files will be downloaded.'),
    )
    
    def handle(self, *args, **options):
        target_names = set(_.strip() for _ in args)
        for cls in DataSource.__subclasses__():
            if cls.__name__ not in target_names:
                continue
            print cls
            cls.refresh(**options)
            