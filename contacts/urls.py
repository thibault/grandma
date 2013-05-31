from django.conf.urls import patterns, include, url


urlpatterns = patterns('contacts.views',
    url(r'^$', 'contact_list', name='contact_list'),
)

