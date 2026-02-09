from rest_framework import serializers

from core.models.study_country import StudyCountry
from context.serializers.country_dto import CountryOutputSerializer
from core.serializers.safety_notification_dto import SafetyNotificationOutputSerializer
from core.serializers.study_ctu_main_details_dto import StudyCTUMainDetailsSerializer


class StudyCountryMainDetailsSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False)
    safety_notifications = SafetyNotificationOutputSerializer(many=True)
    study_ctus = StudyCTUMainDetailsSerializer(many=True)

    class Meta:
        model = StudyCountry
        fields = ['id', 'country', 'study_ctus', 'safety_notifications']