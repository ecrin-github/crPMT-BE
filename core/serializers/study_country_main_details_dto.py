from rest_framework import serializers

from core.models.study_country import StudyCountry
from context.serializers.country_dto import CountryOutputSerializer
from core.serializers.study_ctu_main_details_dto import StudyCTUMainDetailsSerializer


class StudyCountryMainDetailsSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False)
    study_ctus = StudyCTUMainDetailsSerializer(many=True)

    class Meta:
        model = StudyCountry
        fields = ['id', 'country', 'study_ctus', 'lead_country', 'submission_date', 'approval_date']