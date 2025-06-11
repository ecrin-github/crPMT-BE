from rest_framework import serializers

from core.models.project import Project
from core.serializers.study_dto import StudyOutputSerializer


class ProjectInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class ProjectOutputSerializer(serializers.ModelSerializer):
    # date_type = DateTypesOutputSerializer(many=False, read_only=True)
    # last_edited_by = UsersSerializer(many=False, read_only=True)
    studies = StudyOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'