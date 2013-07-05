from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'grandma.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reminders/', include('reminders.urls')),
    url(r'^account/', include('accounts.urls')),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^nexmo/', include('nexmo.urls')),
)
