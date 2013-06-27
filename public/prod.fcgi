#!/usr/bin/python
import os, sys

venv_file = '/home/grandma/.virtualenvs/grandma2/bin/activate_this.py'
if os.path.isfile(venv_file):
    execfile(venv_file, dict(__file__=venv_file))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'grandma'))

os.environ['DJANGO_SETTINGS_MODULE'] = "grandma.settings.prod"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
