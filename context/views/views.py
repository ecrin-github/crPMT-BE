from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from app.permissions import ReadOnly
from context.serializers.country_dto import *
from context.serializers.ctu_dto import *
from context.serializers.funding_source_dto import *
from context.serializers.person_dto import *
from context.serializers.service_dto import *
from context.serializers.study_status_dto import *
from context.models.country import Country
from context.models.ctu import CTU
from context.models.funding_source import FundingSource
from context.models.person import Person
from context.models.service import Service
from context.models.study_status import StudyStatus



class CountryView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Country.objects.all()
    object_class = Country
    serializer_class = CountryOutputSerializer
    permission_classes = [ReadOnly]

    def get_serializer_class(self):
        return super().get_serializer_class()


class CTUView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = CTU.objects.all()
    object_class = CTU
    serializer_class = CTUOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CTUInputSerializer
        return super().get_serializer_class()


class StudyStatusView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = StudyStatus.objects.all()
    object_class = StudyStatus
    serializer_class = StudyStatusOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyStatusInputSerializer
        return super().get_serializer_class()


class FundingSourceView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = FundingSource.objects.all()
    object_class = FundingSource
    serializer_class = FundingSourceOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FundingSourceInputSerializer
        return super().get_serializer_class()


class PersonView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Person.objects.all()
    object_class = Person
    serializer_class = PersonOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PersonInputSerializer
        return super().get_serializer_class()


class ServiceView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Service.objects.all()
    object_class = Service
    serializer_class = ServiceOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ServiceInputSerializer
        return super().get_serializer_class()