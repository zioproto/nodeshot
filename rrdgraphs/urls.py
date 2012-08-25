# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # public
    url(r'^link/(?P<link_id>\d+)$', 'rrdgraphs.views.link', name='rrd_link'),
)
