DATABASES = {
	'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'scrape_games',
        'USER': 'giulio',
        'PASSWORD': '', #usual
        'HOST': 'localhost',
        'PORT': '',
    }
}

CORS_ORIGIN_REGEX_WHITELIST = (r'^(https?://)?(www.)?(\w+\.)?ezgameezlyf.top$', )
