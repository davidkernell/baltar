from settings_live import *

#for pythonanywhere
DATABASE_TYPE = 'mysql'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
if DATABASE_TYPE == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

elif DATABASE_TYPE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'chaturbate_chatlog',
            'USER': 'baltar',
            'PASSWORD': 'Panywherepw!',
            'HOST': 'baltar.mysql.pythonanywhere-services.com',
            'PORT': '3306',
        }
    }
elif DATABASE_TYPE == 'postgres':
    pass
