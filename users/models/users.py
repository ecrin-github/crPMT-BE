import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, db_index=True, null=False, default=uuid.uuid4)
    online = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'
        app_label = 'users'
        verbose_name = 'users'
        verbose_name_plural = 'users'
