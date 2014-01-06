from django.contrib import admin

from .models import Reminder


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'when', 'sent')
    list_filter = ('sent',)
    date_hierarchy = 'created_at'
    readonly_fields = (
        'created_at',
        'when',
        'created_by_ip',
    )
    fields = (
        'sent',
    ) + readonly_fields


admin.site.register(Reminder, ReminderAdmin)
