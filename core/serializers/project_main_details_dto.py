from rest_framework import serializers

from core.models.project import Project


class ProjectMainDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'short_name', 'name', 'ga_number']