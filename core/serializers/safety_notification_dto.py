from rest_framework import serializers

from core.models.safety_notification import SafetyNotification


class SafetyNotificationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = SafetyNotification
        fields = '__all__'


class SafetyNotificationOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = SafetyNotification
        fields = '__all__'
