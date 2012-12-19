from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic.simple import direct_to_template
from unsystem.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ("^$", direct_to_template, {"template": "home.html"}),
    ("^register/$", register),
    ("^confirm/([0-9a-f]{64})$", confirm),
    ("^login/$", login, {"template_name": "login.html"}),
    ("^logout/$", logout, {"next_page": "/"}),
    ("^profile/$", profile),
    ("^tickets/$", tickets),
    ("^info/$", direct_to_template, {"template": "info.html"}),
    ("^contact/$", direct_to_template, {"template": "contact.html"}),
    ("^bio/$", direct_to_template, {"template": "bios.html"}),
    ("^admin/", include(admin.site.urls)),
)
