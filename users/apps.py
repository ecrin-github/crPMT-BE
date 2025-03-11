from django.apps import AppConfig

from configs.app_config import USERS_APP_NAME


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = USERS_APP_NAME
