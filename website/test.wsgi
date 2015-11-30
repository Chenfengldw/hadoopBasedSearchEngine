import sys
sys.path.insert(0, "/var/www/html/search")
from app import app
sys.stdout = sys.stderr
application = app
