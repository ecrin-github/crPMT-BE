from rest_framework import serializers

from context.models.safety_notification_type import SafetyNotificationType


class SafetyNotificationTypeInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = SafetyNotificationType
        fields = '__all__'


class SafetyNotificationTypeOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = SafetyNotificationType
        fields = '__all__'
