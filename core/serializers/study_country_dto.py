from rest_framework import serializers

from core.models.study_country import StudyCountry
from context.serializers.country_dto import CountryOutputSerializer
from core.serializers.study_ctu_dto import StudyCTUOutputSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer


class StudyCountryInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCountry
        fields = '__all__'


class StudyCountryOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False)
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_ctus = StudyCTUOutputSerializer(many=True)


    class Meta:
        model = StudyCountry
        fields = '__all__'