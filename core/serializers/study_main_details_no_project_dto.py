from rest_framework import serializers

from context.serializers.country_dto import CountryOutputSerializer
from context.serializers.organisation_dto import OrganisationOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer
from core.models.study import Study
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer


class StudyMainDetailsNoProjectSerializer(serializers.ModelSerializer): # Used in ProjectMainDetailsSerializer to avoid circular dependencies
    c_euco = PersonOutputSerializer(many=False, read_only=True)
    coordinating_country = CountryOutputSerializer(many=False, read_only=True)
    sponsor_country = CountryOutputSerializer(many=False)
    sponsor_organisation = OrganisationOutputSerializer(many=False)
    study_countries = StudyCountryMainDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = ['id', 'short_title', 'title', 'sponsor_organisation', 'sponsor_country', 'status',
                  'c_euco', 'coordinating_country', 'study_countries', 'uses_ctis_for_safety_notifications']