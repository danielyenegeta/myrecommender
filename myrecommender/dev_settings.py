import dj_database_url
import os
import psycopg2

try:
    from .settings import *
except ImportError:
    pass

DEBUG = False
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
