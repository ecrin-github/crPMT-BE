from rest_framework import serializers

from core.models.study import Study
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer
from core.serializers.study_country_dto import StudyCountryOutputSerializer


class SubmissionInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'


class SubmissionOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Study
        fields = '__all__'
