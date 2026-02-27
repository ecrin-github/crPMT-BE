from django.db import models


class Authority(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'authorities'
        ordering = ['code']

    def create_or_update_authority(authority_code):
        authority, _ = Authority.objects.update_or_create(
            code=authority_code,
            create_defaults={"name": authority_code}    # Sets name as code if authority doesn't exist (create)
        )
        return authority