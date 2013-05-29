from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


urlpatterns = patterns('',
    url(r'^mentions-legales/$',
        TemplateView.as_view(template_name='mentions_legales.html'),
        name='mentions_legales'),
    url(r'^cgv/$',
        TemplateView.as_view(template_name='conditions_generales.html'),
        name='conditions_generales'),
)
