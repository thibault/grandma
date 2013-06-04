from django.conf.urls import patterns, include, url


urlpatterns = patterns('reminders.views',
    url(r'^$', 'pending_reminders', name='pending_reminders'),
    url(r'^sent/$', 'sent_reminders', name='sent_reminders'),
    url(r'^create/$', 'create_reminder', name="create_reminder"),
)
