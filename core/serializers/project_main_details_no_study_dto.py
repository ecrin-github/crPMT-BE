from rest_framework import serializers

from context.serializers.funding_source_dto import FundingSourceOutputSerializer
from context.serializers.organisation_dto import OrganisationOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer
from core.models.project import Project
from core.serializers.reporting_period_dto import ReportingPeriodOutputSerializer
from core.serializers.study_main_details_no_project_dto import StudyMainDetailsNoProjectSerializer


class ProjectMainDetailsNoStudySerializer(serializers.ModelSerializer):
    coordinating_institution = OrganisationOutputSerializer(many=False)
    coordinator = PersonOutputSerializer(many=False)
    funding_sources = FundingSourceOutputSerializer(many=True)
    reporting_periods = ReportingPeriodOutputSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'short_name', 'name', 'start_date', 'end_date', 'coordinating_institution', 
                  'coordinator', 'funding_sources', 'private_funding_details', 'reporting_periods', 'ga_number', 'url']