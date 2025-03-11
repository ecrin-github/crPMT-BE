from rest_framework import serializers

from core.models.study import Study
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer


class StudyMainDetailsSerializer(serializers.ModelSerializer):
    project = ProjectMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'short_title', 'title', 'trial_id', 'project']