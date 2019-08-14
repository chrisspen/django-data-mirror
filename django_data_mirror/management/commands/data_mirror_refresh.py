#!/usr/bin/env python
from optparse import make_option

# from django.conf import settings
from django.core.management.base import BaseCommand

from django_data_mirror.models import DataSourceControl


class Command(BaseCommand):
    help = 'Updated models storing data from an external source.'
    args = '<target names>'
    option_list = BaseCommand.option_list + (
        make_option('--bulk', dest='bulk', action='store_true', default=False, help='If given, attempts to download bulk data instead of incrementally.'),
        make_option('--fn', dest='fn', help='If given, the local filename to use.'),
        make_option('--skip-to', dest='skip_to', help='A record indicator that the backend processor should start from.'),
        make_option('--no-download', dest='no_download', action='store_true', default=False, help='If given, no files will be downloaded.'),
        make_option(
            '--force',
            action='store_true',
            default=False,
            help='Signals to the backend that files should be processed even if they are already marked as complete.'
        ),
        make_option('--ids', dest='ids', help='A comma-delimited list of IDs to solely refresh.'),
    )

    def handle(self, *args, **options):
        DataSourceControl.populate()
        q = DataSourceControl.objects.get_enabled()
        slugs = set(_.strip() for _ in args)
        if slugs:
            q = q.filter(slug__in=slugs)
        total = q.count()

        ids = [_.strip() for _ in (options['ids'] or '').split(',') if _.strip()]
        options['ids'] = ids

        i = 0
        for control in q.iterator():
            i += 1
            print('Processing %s (%i of %i)' % (control.slug, i, total))
            control.refresh(**options)
