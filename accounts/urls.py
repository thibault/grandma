from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout_then_login


urlpatterns = patterns('accounts.views',
    url(r'^$', 'my_account', name='my_account'),
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),
    url(r'^password/reset/$', 'password_reset', name='password_reset'),
    url(r'^password/reset/confirm/(?P<activation_key>\w+)$', 'password_reset_confirm', name='password_reset_confirm'),
)
