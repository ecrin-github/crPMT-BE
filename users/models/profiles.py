import uuid

from django.db import models

from users.models.users import Users


class UserProfiles(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='user_profile',
                                db_column='user_id', default=None, null=True, blank=True)
    ls_aai_id = models.CharField(max_length=255, null=True, blank=True)
    # prof_title = models.CharField(max_length=25, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    # inverted_full_name = models.CharField(max_length=255, null=True, blank=True)
    # orcid = models.CharField(max_length=75, null=True, blank=True)
    # designation = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'user_profiles'
        ordering = ['id']
