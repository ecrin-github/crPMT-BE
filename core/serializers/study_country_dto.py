from rest_framework import serializers

from core.models.study_country import StudyCountry
from context.serializers.country_dto import CountryOutputSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer
from core.serializers.study_ctu_main_details_dto import StudyCTUMainDetailsSerializer


class StudyCountryInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCountry
        fields = '__all__'


class StudyCountryOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False)
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_ctus = StudyCTUMainDetailsSerializer(many=True)


    class Meta:
        model = StudyCountry
        fields = '__all__'