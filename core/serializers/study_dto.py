from rest_framework import serializers

from core.models.study import Study
from context.serializers.person_dto import PersonOutputSerializer
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer
from core.serializers.study_country_dto import StudyCountryOutputSerializer


class StudyInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'


class StudyOutputSerializer(serializers.ModelSerializer):
    project = ProjectMainDetailsSerializer(many=False, read_only=True)
    pi = PersonOutputSerializer(many=False, read_only=True)
    study_countries = StudyCountryOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = '__all__'