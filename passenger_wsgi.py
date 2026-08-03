import os
import sys

PROJECT_ROOT = "/home/bpkadksb/garda.kabsumbawabarat.com/"

sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "PYmodule.settings"
)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
