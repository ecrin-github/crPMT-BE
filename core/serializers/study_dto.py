from rest_framework import serializers

from context.models.complex_trial_type import ComplexTrialType
from context.models.medical_field import MedicalField
from context.models.population import Population
from context.models.service import Service
from context.serializers.complex_trial_type_dto import ComplexTrialTypeOutputSerializer
from context.serializers.country_dto import CountryOutputSerializer
from context.serializers.medical_field_dto import MedicalFieldOutputSerializer
from context.serializers.organisation_dto import OrganisationOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer
from context.serializers.population_dto import PopulationOutputSerializer
from context.serializers.service_dto import ServiceOutputSerializer
from core.models.study import Study
from core.serializers.project_main_details_dto import ProjectMainDetailsSerializer
from core.serializers.study_country_dto import StudyCountryOutputSerializer


class StudyInputSerializer(serializers.ModelSerializer):
    medical_fields = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MedicalField.objects.all())
    populations = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Population.objects.all())
    services = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Service.objects.all())

    class Meta:
        model = Study
        fields = '__all__'


class StudyOutputSerializer(serializers.ModelSerializer):
    c_euco = PersonOutputSerializer(many=False, read_only=True)
    complex_trial_type = ComplexTrialTypeOutputSerializer
    coordinating_country = CountryOutputSerializer(many=False, read_only=True)
    medical_fields = MedicalFieldOutputSerializer(many=True)
    pi = PersonOutputSerializer(many=False, read_only=True)
    populations = PopulationOutputSerializer(many=True)
    project = ProjectMainDetailsSerializer(many=False, read_only=True)
    services = ServiceOutputSerializer(many=True)
    sponsor_country = CountryOutputSerializer(many=False)
    sponsor_organisation = OrganisationOutputSerializer(many=False)
    study_countries = StudyCountryOutputSerializer(many=True, read_only=True)

    class Meta:
        model = Study
        fields = '__all__'