#!/usr/bin/env python
# coding: utf-8
import os
import sys
from django.core.handlers.wsgi import WSGIHandler


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
application = WSGIHandler()
