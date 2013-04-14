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
        'NAME': 'ProvinceManagement',             # Or path to database file if using sqlite3.
        'USER': 'root',                       # Not used with sqlite3.
        'PASSWORD': 'root',                   # Not used with sqlite3.
        'HOST': '192.168.20.100',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                           # Set to empty string for default. Not used with sqlite3.
    }
}

WEB_TITLE = "Province Management Pro"

#send 404 link to admin user
SEND_BROKEN_LINK_EMAILS = True

# Set your DSN value
RAVEN_CONFIG = {
        'dsn': 'http://e73fc4cdbe3243fd9cfe2160df1826a9:2e1cd656d69145e397c484bcdc9cc91a@192.168.2.7:19000/2',
    }

# Add raven to the list of installed apps
INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
        )
