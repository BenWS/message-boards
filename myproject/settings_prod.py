from decouple import config, Csv
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

