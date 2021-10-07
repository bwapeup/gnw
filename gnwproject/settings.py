import os
from decouple import config, Csv

# Basic Django settings
#----------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gnw',
    'sms',
    'people',
    'enrollment',
    'progress',
    'session_control',
    'admin_honeypot',
    'captcha',
    #'debug_toolbar',
]

MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'session_control.middleware.PreventConcurrentLoginsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gnwproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG
        },
    },
]

WSGI_APPLICATION = 'gnwproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

#Starting with Django 3.2, the datatype of implicit primary fields must
#be specified in the settings file. 
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTHENTICATION_BACKENDS = [
    'people.backends.MobileBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'sms.validators.AtLeastOneNumberPasswordValidator',
    },
]
#----------------------------------------------------------



# Email
#----------------------------------------------------------

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

#DEFAULT_FROM_EMAIL = 'Feimao <noreply@feimaoclasstest.xyz>'
EMAIL_SUBJECT_PREFIX = '[Feimao System] '
#----------------------------------------------------------



# Admins and Managers
#----------------------------------------------------------

ADMINS = [('Admin', config('FEIMAO_ADMIN_EMAIL', default=''))]
MANAGERS = [('Manager', config('FEIMAO_MANAGER_EMAIL', default=''))]
#----------------------------------------------------------



# Internationalization
#----------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#----------------------------------------------------------


# Static files
#----------------------------------------------------------
#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'gnw/static'),
#    os.path.join(BASE_DIR, 'sms/static'),
#]

AWS_STATIC_FOLDER = 'static'
#AWS_LOCATION = 'assignments'
AWS_ACCESS_KEY_ID = config('AWS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET_NAME')
AWS_REGION = config('AWS_REGION')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
#AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400',}
#STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_FOLDER)
#AWS_CLOUDFRONT_DOMAIN = config('AWS_CLOUDFRONT_DOMAIN')
#STATIC_URL = 'https://%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, AWS_LOCATION)


# Security
#----------------------------------------------------------
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
#SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
X_FRAME_OPTIONS = 'DENY'
#----------------------------------------------------------


# Yunpian SMS
#----------------------------------------------------------
#YUNPIAN_APIKEY = config('YUNPIAN_APIKEY')
#----------------------------------------------------------


# Admin Honeypot
#----------------------------------------------------------
ADMIN_HONEYPOT_EMAIL_ADMINS = False
#----------------------------------------------------------


# Django Simple Captcha
#----------------------------------------------------------
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_dots',)
CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s %(hidden_field)s %(image)s'
#----------------------------------------------------------


# Miscellaneous
#----------------------------------------------------------
LOGIN_REDIRECT_URL = '/panel'  
LOGOUT_REDIRECT_URL = '/accounts/login'
AUTH_USER_MODEL = 'people.CustomUser'
#----------------------------------------------------------

#For django debug toolbar
#----------------------------------------------------------
INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]
#----------------------------------------------------------

#Cloud storage backend
#----------------------------------------------------------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#----------------------------------------------------------