"""
WSGI config for collab_coursebook project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

"""
sys.path.append('/srv/collab-coursebook/collab-coursebook')
sys.path.append('/src/collab-coursebook/venv/lib/python3.7/site-packages')
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collab_coursebook.settings')

application = get_wsgi_application()


