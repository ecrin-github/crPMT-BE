from rest_framework import serializers

from core.models.project import Project
from core.serializers.study_main_details_no_project_dto import StudyMainDetailsNoProjectSerializer


class ProjectMainDetailsSerializer(serializers.ModelSerializer):
    studies = StudyMainDetailsNoProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'short_name', 'name', 'ga_number', 'studies']