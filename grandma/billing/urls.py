from django.conf.urls import patterns, url


urlpatterns = patterns(
    'billing.views',
    url(r'^upgrade-plan$', 'upgrade_plan', name='upgrade_plan'),
)
