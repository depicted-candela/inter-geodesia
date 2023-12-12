"""
WSGI config for geodesia project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os, jpype
from django.core.wsgi import get_wsgi_application

jpype.startJVM(classpath=['/home/depiction/geodesia/JToolsQgeoid/bin/',
                        '/home/depiction/Documents/libraries/TinfourCore-2.1.7.jar'])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodesia.settings')

application = get_wsgi_application()
