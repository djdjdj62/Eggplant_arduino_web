"""
WSGI config for arduino_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/

mysite

arduino_web
"""

import os

from django.core.wsgi import get_wsgi_application

from dj_static import Cling 


import sys

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if path not in sys.path:
    sys.path.append(path)

    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arduino_web.settings')

application = Cling(get_wsgi_application())
