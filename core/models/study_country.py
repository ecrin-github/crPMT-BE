import datetime

from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from context.models.country import Country
from core.models.safety_notification import SafetyNotification
from core.models.study import Study


class StudyCountry(models.Model):
    id = models.BigAutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE,
                                db_column='study_id', blank=True, null=True,
                                related_name='study_countries', default=None)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, to_field="iso2",
                                    db_column='country_id', blank=True, null=True,
                                    related_name='study_countries', default=None)
    safety_notifications = models.ManyToManyField(SafetyNotification, blank=True)
    order = models.IntegerField(blank=True, null=True, db_column='order')

    # def sync_shared_safety_notifications(self):
    #     if self._pending_safety_notification_pks:
    #         current_safety_notifications = SafetyNotification.objects.filter(pk__in=self._pending_safety_notification_pks)
    #     else:
    #         current_safety_notifications = list(self.refresh_from_db().safety_notifications.all())
        
    #     # Update CTIS SCs
    #     study_countries = StudyCountry.objects.filter(study=self.study).exclude(pk=self.pk)
    #         for study_country in study_countries:
    #             if study_country.country and study_country.country.is_in_eea and study_country.country.is_in_eu:
    #                 # Syncing CTIS SCs SNs
    #                 study_country.safety_notifications.set(self.safety_notifications.all())
    #                 study_country._pending_safety_notification_pks = [] # TODO: ?
    #                 study_country.save(update_fields=["_pending_safety_notification_pks"])
    


    # def save(self, *args, **kwargs):
    #     super(StudyCountry, self).save(*args, **kwargs)

    #     # Note (TODO): this code is currently redundant for edits from the study page, this is only needed for when updating
    #     # from a single study country page, but there is no way here to know if this is an update from the study or study country page
    #     if self.pk and self.study.uses_ctis_for_safety_notifications and self.country and self.country.is_in_eea and self.country.is_in_eu:
    #         study_countries = StudyCountry.objects.filter(study=self.study).exclude(pk=self.pk)
    #         for study_country in study_countries:
    #             if study_country.country and study_country.country.is_in_eea and study_country.country.is_in_eu:
    #                 # Syncing CTIS SCs SNs
    #                 study_country.safety_notifications.set(self.safety_notifications.all())

    class Meta:
        db_table = 'study_countries'
        ordering = ['order']


# @receiver(m2m_changed, sender=StudyCountry.safety_notifications.through)
# def sync_shared_cs_on_m2m(sender, instance, action, pk_set, **kwargs):
#     if action in ['post_add', 'post_remove', 'post_clear']:
#         if instance.country and instance.country.is_in_eea and instance.country.is_in_eu and instance.study.uses_ctis_for_safety_notifications:
#             current_sns = list(instance.safety_notifications.all())
            
#             study_countries = StudyCountry.objects.filter(study=instance.study)
#             for study_country in study_countries:
#                 if study_country.country and study_country.country.is_in_eea and study_country.country.is_in_eu:
#                     # Syncing CTIS SCs SNs
#                     study_country.safety_notifications.set(current_sns)