from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined')
    readonly_fields = (
        'date_joined',
        'paymill_client_id',
        'paymill_card_id',
        'paymill_subscription_id',
    )
    fields = (
        'email',
        'phone',
        'is_superuser',
    ) + readonly_fields


admin.site.register(User, UserAdmin)
