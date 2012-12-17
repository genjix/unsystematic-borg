from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from unsystem.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url("^$", direct_to_template, {"template": "home.html"}),
    # Examples:
    # url(r'^$', 'unsystem.views.home', name='home'),
    # url(r'^unsystem/', include('unsystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)