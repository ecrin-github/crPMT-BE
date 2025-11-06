from rest_framework import serializers

from context.models.funding_source import FundingSource
from context.models.service import Service
from context.serializers.funding_source_dto import FundingSourceOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer
from context.serializers.organisation_dto import OrganisationOutputSerializer
from core.models.project import Project
from core.serializers.study_dto import StudyOutputSerializer


class ProjectInputSerializer(serializers.ModelSerializer):
    funding_sources = serializers.PrimaryKeyRelatedField(
        many=True, queryset=FundingSource.objects.all())

    class Meta:
        model = Project
        fields = '__all__'


class ProjectOutputSerializer(serializers.ModelSerializer):
    coordinating_institution = OrganisationOutputSerializer(many=False)
    coordinator = PersonOutputSerializer(many=False)
    funding_sources = FundingSourceOutputSerializer(many=True)
    studies = StudyOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'