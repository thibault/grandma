from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login


urlpatterns = patterns('accounts.views',
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^forgot_password/$', 'send_password', name='send_password'),
)
