import sys
import os

# Add the project base directory to the sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'esports_portfolio.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 