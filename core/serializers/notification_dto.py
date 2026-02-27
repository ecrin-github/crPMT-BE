from rest_framework import serializers

from context.models.authority import Authority
from context.serializers.authority_dto import AuthorityOutputSerializer
from core.models.notification import Notification
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class NotificationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'

    def to_internal_value(self, data):
        # Skip authority validation otherwise would get an "already exists" error if authority already exists
        authority_code = data.pop('authority', None)
        result = super().to_internal_value(data)
        result['authority_code'] = authority_code
        return result

    def create(self, validated_data):
        authority_code = validated_data.pop('authority_code', None)
        if authority_code is not None:
            validated_data['authority'] = Authority.create_or_update_authority(authority_code)
        
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        authority_code = validated_data.pop('authority_code', None)
        
        if authority_code is not None:
            instance.authority = Authority.create_or_update_authority(authority_code)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    

class NotificationOutputSerializer(serializers.ModelSerializer):
    study_country = StudyCountryMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
