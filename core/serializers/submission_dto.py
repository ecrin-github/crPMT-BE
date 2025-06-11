from rest_framework import serializers

from core.models.study import Study
from context.serializers.country_dto import CountryOutputSerializer


class SubmissionInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'


class SubmissionOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Study
        fields = '__all__'
