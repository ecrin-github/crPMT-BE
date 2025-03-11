from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers.project_dto import *
from core.serializers.study_dto import *
from core.serializers.study_country_dto import *
from core.models.project import Project
from core.models.study import Study
from core.models.study_country import StudyCountry


class ProjectView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Project.objects.all()
    object_class = Project
    serializer_class = ProjectOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectInputSerializer
        return super().get_serializer_class()


class StudyView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Study.objects.all()
    object_class = Study
    serializer_class = StudyOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyInputSerializer
        return super().get_serializer_class()


class StudyCountryView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = StudyCountry.objects.all()
    object_class = StudyCountry
    serializer_class = StudyCountryOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyCountryInputSerializer
        return super().get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return StudyCountry.objects.none()
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(study=self.kwargs['studyId'])
        )