from django.conf.urls import patterns, include, url


urlpatterns = patterns('reminders.views',
    url(r'^$', 'home', name="home"),
)