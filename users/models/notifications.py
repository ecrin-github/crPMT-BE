import uuid
import datetime

from django.db import models

from users.models.users import Users


class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True, unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id', blank=False)
    datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)

    class Meta:
        db_table = 'user_notifications'
