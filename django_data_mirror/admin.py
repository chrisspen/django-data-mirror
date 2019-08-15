# from django.conf import settings
from django.contrib import admin

from . import models


class DataSourceControlAdmin(admin.ModelAdmin):

    list_display = (
        'slug',
        'enabled',
    )

    list_filter = ('enabled',)

    search_fields = ('slug',)


admin.site.register(models.DataSourceControl, DataSourceControlAdmin)


class DataSourceFileAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'source',
        'total_lines',
        'total_lines_complete',
        #        'percent',
        'percent_str',
        'downloaded',
        'complete',
    )

    list_filter = ('complete',)

    raw_id_fields = ('source',)

    search_fields = ('name',)

    readonly_fields = ('percent_str',)

    def percent_str(self, obj=None):
        if not obj:
            return ''
        return '%.02f' % (obj.percent,)

    percent_str.short_description = 'percent'
    percent_str.admin_order_field = 'percent'


admin.site.register(models.DataSourceFile, DataSourceFileAdmin)
