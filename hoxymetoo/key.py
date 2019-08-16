mysql_conf = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hoxymetoo',
    'USER': 'webserver',
    'PASSWORD': 'webserver?',
    'HOST': 'localhost',
    'PORT': '3306',
    'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    },
}
