from django.apps import AppConfig

from configs.app_config import CORE_APP_NAME


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = CORE_APP_NAME
