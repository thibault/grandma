from django.conf.urls import patterns, include, url


urlpatterns = patterns('reminders.views',
    url(r'^$', 'create_reminder', name="create_reminder"),
    url(r'^reminders/$', 'reminder_list', name='reminder_list'),
)
