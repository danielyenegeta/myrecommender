from .base import *
import dj_database_url
DEBUG = False
SECRET_KEY=os.environ['SECRET_KEY']
DATABASES = {}
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
