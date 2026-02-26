from rest_framework import serializers

from core.models.study import Study
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class StudyMainDetailsNoProjectSerializer(serializers.ModelSerializer): # Used in ProjectMainDetailsSerializer to avoid circular dependencies
    study_countries = StudyCountryMainDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'short_title', 'title', 'study_countries', 'uses_ctis_for_safety_notifications']