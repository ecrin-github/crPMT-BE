from rest_framework import serializers

from core.models.notification import Notification
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class NotificationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationOutputSerializer(serializers.ModelSerializer):
    study_country = StudyCountryMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
