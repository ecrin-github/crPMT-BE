from rest_framework import serializers

from core.models.safety_notification import SafetyNotification
from core.models.study_country import StudyCountry
from context.serializers.country_dto import CountryOutputSerializer
from core.serializers.notification_dto import NotificationOutputSerializer
from core.serializers.safety_notification_dto import SafetyNotificationOutputSerializer
from core.serializers.study_ctu_dto import StudyCTUOutputSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer
from core.serializers.submission_dto import SubmissionOutputSerializer


class StudyCountryInputSerializer(serializers.ModelSerializer):
    safety_notifications = serializers.PrimaryKeyRelatedField(
        many=True, queryset=SafetyNotification.objects.all())
    
    class Meta:
        model = StudyCountry
        fields = '__all__'


class StudyCountryOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False)
    notifications = NotificationOutputSerializer(many=True)
    safety_notifications = SafetyNotificationOutputSerializer(many=True)
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_ctus = StudyCTUOutputSerializer(many=True)
    submissions = SubmissionOutputSerializer(many=True)

    class Meta:
        model = StudyCountry
        fields = '__all__'