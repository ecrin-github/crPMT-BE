from rest_framework import serializers

from core.models.study import Study
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class StudyMainDetailsSerializer(serializers.ModelSerializer):
    project = ProjectMainDetailsSerializer(many=False, read_only=True)
    study_countries = StudyCountryMainDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'short_title', 'title', 'project', 'study_countries', 'uses_ctis_for_safety_notifications']