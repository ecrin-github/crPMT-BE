from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.permissions import ReadOnly
from context.serializers.authority_dto import *
from context.serializers.complex_trial_type_dto import *
from context.serializers.country_dto import *
from context.serializers.ctu_dto import *
from context.serializers.hospital_dto import *
from context.serializers.funding_source_dto import *
from context.serializers.medical_field_dto import *
from context.serializers.organisation_dto import *
from context.serializers.person_dto import *
from context.serializers.population_dto import *
from context.serializers.regulatory_framework_detail_dto import *
from context.serializers.safety_notification_type_dto import *
from context.serializers.service_dto import *
from context.serializers.study_status_dto import *

from context.models.authority import *
from context.models.complex_trial_type import *
from context.models.country import *
from context.models.ctu import *
from context.models.hospital import *
from context.models.funding_source import *
from context.models.medical_field import *
from context.models.organisation import *
from context.models.person import *
from context.models.population import *
from context.models.regulatory_framework_detail import *
from context.models.safety_notification_type import *
from context.models.service import *
from context.models.study_status import *



class AuthorityView(viewsets.ModelViewSet):
    queryset = Authority.objects.all()
    object_class = Authority
    serializer_class = AuthorityOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AuthorityInputSerializer
        return super().get_serializer_class()


class ComplexTrialTypeView(viewsets.ModelViewSet):
    queryset = ComplexTrialType.objects.all()
    object_class = ComplexTrialType
    serializer_class = ComplexTrialTypeOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ComplexTrialTypeInputSerializer
        return super().get_serializer_class()


class CountryView(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    object_class = Country
    serializer_class = CountryOutputSerializer
    permission_classes = [ReadOnly]

    def get_serializer_class(self):
        return super().get_serializer_class()


class CTUView(viewsets.ModelViewSet):
    queryset = CTU.objects.all()
    object_class = CTU
    serializer_class = CTUOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CTUInputSerializer
        return super().get_serializer_class()


class HospitalView(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    object_class = Hospital
    serializer_class = HospitalOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return HospitalInputSerializer
        return super().get_serializer_class()


class FundingSourceView(viewsets.ModelViewSet):
    queryset = FundingSource.objects.all()
    object_class = FundingSource
    serializer_class = FundingSourceOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FundingSourceInputSerializer
        return super().get_serializer_class()


class MedicalFieldView(viewsets.ModelViewSet):
    queryset = MedicalField.objects.all()
    object_class = MedicalField
    serializer_class = MedicalFieldOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return MedicalFieldInputSerializer
        return super().get_serializer_class()


class OrganisationView(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    object_class = Organisation
    serializer_class = OrganisationOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrganisationInputSerializer
        return super().get_serializer_class()


class PersonView(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    object_class = Person
    serializer_class = PersonOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PersonInputSerializer
        return super().get_serializer_class()


class PopulationView(viewsets.ModelViewSet):
    queryset = Population.objects.all()
    object_class = Population
    serializer_class = PopulationOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PopulationInputSerializer
        return super().get_serializer_class()


class RegulatoryFrameworkDetailView(viewsets.ModelViewSet):
    queryset = RegulatoryFrameworkDetail.objects.all()
    object_class = RegulatoryFrameworkDetail
    serializer_class = RegulatoryFrameworkDetailOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return RegulatoryFrameworkDetailInputSerializer
        return super().get_serializer_class()


class SafetyNotificationTypeView(viewsets.ModelViewSet):
    queryset = SafetyNotificationType.objects.all()
    object_class = SafetyNotificationType
    serializer_class = SafetyNotificationTypeOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SafetyNotificationTypeInputSerializer
        return super().get_serializer_class()


class ServiceView(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    object_class = Service
    serializer_class = ServiceOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ServiceInputSerializer
        return super().get_serializer_class()


class StudyStatusView(viewsets.ModelViewSet):
    queryset = StudyStatus.objects.all()
    object_class = StudyStatus
    serializer_class = StudyStatusOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyStatusInputSerializer
        return super().get_serializer_class()