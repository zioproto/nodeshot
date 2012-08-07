#!/usr/bin/env python

import urllib2, sys, os

# determine directory automatically
directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.abspath(os.path.join(directory, os.path.pardir, os.path.pardir))
sys.path.append(parent)

import settings
from django.core.management import setup_environ
setup_environ(settings)
__builtins__.IS_SCRIPT = True
#from nodeshot.models import *
#from django.db.models import Q

from nodeshot.models import Interface
i = Interface.objects.all()
print i
