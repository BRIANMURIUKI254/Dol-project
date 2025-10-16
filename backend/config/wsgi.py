"""
WSGI config for Days of Light (D.O.L) ministry backend.
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add project directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# This application object is used by the development server and any WSGI server
application = get_wsgi_application()

# Apply WSGI middleware here if needed
# from whitenoise import WhiteNoise
# application = WhiteNoise(application, root=os.path.join(project_root, 'staticfiles'))
# application.add_files(os.path.join(project_root, 'media'), prefix='media/')
