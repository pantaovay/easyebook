import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

import sae
from easyebook import wsgi
from sae.ext.shell import ShellMiddleware

application = sae.create_wsgi_app(ShellMiddleware(wsgi.application))
