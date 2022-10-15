# settings/local.py
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_1e96w@!3ci9h7*3!v&is$bzze$hn9-axqm(0b5+yi9)6n-@1%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com']