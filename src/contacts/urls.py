from django.conf.urls import patterns, include, url


urlpatterns = patterns('contacts.views',
    url(r'^$', 'contact_list', name='contact_list'),
    url(r'^search.json$', 'contact_list_json', name='contact_list_json'),
)

