import sys
assert sys.version_info.major >= 3, "Python version too old in anna.wsgi!"

sys.path.insert(0, '/home/anna/public_wsgi/')
from mealApp import app as application
