from rest_framework import serializers

from context.models.authority import Authority
from context.serializers.authority_dto import AuthorityInputSerializer, AuthorityOutputSerializer
from core.models.submission import Submission
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class SubmissionInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submission
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
        
        return Submission.objects.create(**validated_data)

    def update(self, instance, validated_data):
        authority_code = validated_data.pop('authority_code', None)
        
        if authority_code is not None:
            instance.authority = Authority.create_or_update_authority(authority_code)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance


class SubmissionOutputSerializer(serializers.ModelSerializer):
    study_country = StudyCountryMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'