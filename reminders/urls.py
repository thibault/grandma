from django.conf.urls import patterns, include, url


urlpatterns = patterns('reminders.views',
    url(r'^$', 'reminder_list', name='reminder_list'),
    url(r'^create/$', 'create_reminder', name="create_reminder"),
)
