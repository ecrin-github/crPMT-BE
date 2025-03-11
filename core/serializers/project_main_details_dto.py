from rest_framework import serializers

from core.models.project import Project


class ProjectMainDetailsSerializer(serializers.ModelSerializer):
    # date_type = DateTypesOutputSerializer(many=False, read_only=True)
    # last_edited_by = UsersSerializer(many=False, read_only=True)
    # study = StudyOutputMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'short_name', 'name', 'ga_number']