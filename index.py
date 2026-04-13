import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hotel_project.settings")

# Import the WSGI application
from django.core.wsgi import get_wsgi_application

# Vercel requires a variable named "app"
app = get_wsgi_application()
