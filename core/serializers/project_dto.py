from rest_framework import serializers

from context.models.funding_source import FundingSource
from context.models.service import Service
from core.models.project import Project
from context.serializers.funding_source_dto import FundingSourceOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer
from context.serializers.service_dto import ServiceOutputSerializer
from core.serializers.study_dto import StudyOutputSerializer


class ProjectInputSerializer(serializers.ModelSerializer):
    funding_sources = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FundingSource.objects.all())
    services = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Service.objects.all())

    class Meta:
        model = Project
        fields = '__all__'


class ProjectOutputSerializer(serializers.ModelSerializer):
    # date_type = DateTypesOutputSerializer(many=False, read_only=True)
    # last_edited_by = UsersSerializer(many=False, read_only=True)
    funding_sources = FundingSourceOutputSerializer(many=True)
    services = ServiceOutputSerializer(many=True)
    studies = StudyOutputSerializer(many=True, read_only=True)
    c_euco = PersonOutputSerializer(many=False)

    class Meta:
        model = Project
        fields = '__all__'