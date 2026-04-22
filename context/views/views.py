from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from context.services.ctu_service import resolve_ctu_from_sharepoint
from rest_framework import viewsets, permissions

from app.permissions import ReadOnly
from context.models.ctu_status import CTUStatus
from context.serializers.authority_dto import *
from context.serializers.complex_trial_type_dto import *
from context.serializers.country_dto import *
from context.serializers.ctu_dto import *
from context.serializers.ctu_status_dto import CTUStatusInputSerializer, CTUStatusOutputSerializer
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
from context.serializers.visit_type_dto import *

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
from context.models.visit_type import *



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


class CTUStatusView(viewsets.ModelViewSet):
    queryset = CTUStatus.objects.all()
    object_class = CTUStatus
    serializer_class = CTUStatusOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CTUStatusInputSerializer
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


class VisitTypeView(viewsets.ModelViewSet):
    queryset = VisitType.objects.all()
    object_class = VisitType
    serializer_class = VisitTypeOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VisitTypeInputSerializer
        return super().get_serializer_class()

class ResolveSharePointCTUView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sharepoint_item_id = request.data.get("sharepoint_item_id")
        name = request.data.get("name")
        short_name = request.data.get("short_name")
        country_iso2 = request.data.get("country_iso2")
        sas_verification = request.data.get("sas_verification", False)
        address_info = request.data.get("address_info")

        if not country_iso2:
            return Response(
                {"detail": "country_iso2 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        country = Country.objects.filter(iso2=country_iso2).first()
        if not country:
            return Response(
                {"detail": f"Country not found for iso2={country_iso2}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = {
            "sharepoint_item_id": sharepoint_item_id,
            "name": name,
            "short_name": short_name,
            "country": country,
            "sas_verification": sas_verification,
            "address_info": address_info,
            "contact": None,  # it can be set later manually if needed
        }

        ctu = resolve_ctu_from_sharepoint(payload)

        return Response({
            "id": ctu.id,
            "sharepoint_item_id": ctu.sharepoint_item_id,
            "name": ctu.name,
            "short_name": ctu.short_name,
            "country_iso2": ctu.country.iso2 if ctu.country else None,
            "sas_verification": ctu.sas_verification,
            "address_info": ctu.address_info,
        })
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sharepoint_item_id = request.data.get("sharepoint_item_id")
        name = request.data.get("name")
        short_name = request.data.get("short_name")
        country_iso2 = request.data.get("country_iso2")
        sas_verification = request.data.get("sas_verification", False)

        if not country_iso2:
            return Response(
                {"detail": "country_iso2 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        country = Country.objects.filter(iso2=country_iso2).first()
        if not country:
            return Response(
                {"detail": f"Country not found for iso2={country_iso2}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = {
            "sharepoint_item_id": sharepoint_item_id,
            "name": name,
            "short_name": short_name,
            "country": country,
            "sas_verification": sas_verification,
        }

        ctu = resolve_ctu_from_sharepoint(payload)

        return Response({
            "id": ctu.id,
            "sharepoint_item_id": ctu.sharepoint_item_id,
            "name": ctu.name,
            "short_name": ctu.short_name,
            "country_iso2": ctu.country.iso2 if ctu.country else None,
            "sas_verification": ctu.sas_verification,
        })