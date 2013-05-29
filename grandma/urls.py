from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'reminders.views.create_reminder', name='home'),
    url(r'^reminders/', include('reminders.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^pages/', include('pages.urls')),
)
