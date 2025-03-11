from rest_framework import serializers

from core.models.study import Study
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer
from core.serializers.study_country_dto import StudyCountryOutputSerializer


class StudyInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Study
        fields = '__all__'


class StudyOutputSerializer(serializers.ModelSerializer):
    # date_type = DateTypesOutputSerializer(many=False, read_only=True)
    # last_edited_by = UsersSerializer(many=False, read_only=True)
    project = ProjectMainDetailsSerializer(many=False, read_only=True)
    study_countries = StudyCountryOutputSerializer(many=True, read_only=False)

    class Meta:
        model = Study
        fields = '__all__'
