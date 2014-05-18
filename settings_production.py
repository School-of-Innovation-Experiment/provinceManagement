"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: Django setting for daily development
    Created: 2013-4-12
"""

from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'SchoolTest',             # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'root',                   # Not used with sqlite3.
        'HOST': '192.168.20.100',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}

WEB_TITLE = "School Management Pro"

#send 404 link to admin user
SEND_BROKEN_LINK_EMAILS = True

# Set your DSN value
# RAVEN_CONFIG = {
#         'dsn': 'http://7df69c0bb5924480bd95b0616413c85d:3583f76fc35a473cb35f595e381915eb@192.168.2.7:19000/3',
#     }

# # Add raven to the list of installed apps
# INSTALLED_APPS = INSTALLED_APPS + (
#         'raven.contrib.django.raven_compat',
#         )
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
#     'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
#     )
