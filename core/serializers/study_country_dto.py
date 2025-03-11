from rest_framework import serializers

from core.models.study_country import StudyCountry
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer


class StudyCountryInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyCountry
        fields = '__all__'


class StudyCountryOutputSerializer(serializers.ModelSerializer):
    # date_type = DateTypesOutputSerializer(many=False, read_only=True)
    # last_edited_by = UsersSerializer(many=False, read_only=True)
    study = StudyMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = StudyCountry
        fields = '__all__'


