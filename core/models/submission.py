import datetime

from django.db import models

from context.models.authority import Authority
from core.models.study_country import StudyCountry


class Submission(models.Model): # Initial submission, amendment, or other notification
    id = models.BigAutoField(primary_key=True)
    authority = models.ForeignKey(Authority, on_delete=models.SET_NULL,
                                db_column='authority_id', blank=True, null=True,
                                related_name='submissions', default=None)
    not_applicable = models.BooleanField(default=False) # Only for initial submissions that are not EC authority
    submission_date = models.DateTimeField(blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    protocol_approval_date = models.DateTimeField(blank=True, null=True)
    protocol_approved_version = models.CharField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    is_other_notification = models.BooleanField(default=False)
    is_amendment = models.BooleanField(default=False)
    amendment_reason = models.CharField(blank=True, null=True)
    study_country = models.ForeignKey(StudyCountry, on_delete=models.CASCADE,
                                db_column='study_country_id', blank=True, null=True,
                                related_name='submissions', default=None)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    class Meta:
        db_table = 'submissions'
        ordering = ['order']