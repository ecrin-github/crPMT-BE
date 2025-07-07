from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from context.serializers.ctu_dto import *
from core.serializers.project_dto import *
from core.serializers.study_dto import *
from core.serializers.study_country_dto import *
from core.serializers.study_ctu_dto import *
from core.serializers.visit_dto import *
from context.models.ctu import CTU
from context.models.person import Person
from core.models.project import Project
from core.models.study import Study
from core.models.study_country import StudyCountry
from core.models.study_ctu import StudyCTU
from core.models.visit import Visit


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
        if 'sId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study=self.kwargs['sId'])
            )
        return super().get_queryset(*args, **kwargs)


class StudyCTUView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = StudyCTU.objects.all()
    object_class = StudyCTU
    serializer_class = StudyCTUOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyCTUInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return StudyCountry.objects.none()
        if 'sId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study=self.kwargs['sId'])
            )
        if 'scId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_country=self.kwargs['scId'])
            )
        return super().get_queryset(*args, **kwargs)


class VisitView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Visit.objects.all()
    object_class = Visit
    serializer_class = VisitOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VisitInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return StudyCountry.objects.none()
        if 'sId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_ctu=self.kwargs['sId'])
            )
        if 'sctuId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_ctu=self.kwargs['sctuId'])
            )
        return super().get_queryset(*args, **kwargs)


class ProjectsByFundingSource(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, fs_id):
        if not fs_id:
            return Response({'error': "fs_id (funding source id) param is missing"})

        fs_check = FundingSource.objects.filter(id=fs_id)

        if not fs_check.exists():
            return Response({'error': f"Funding source with the id {fs_id} does not exist."})

        projects = Project.objects.filter(funding_sources__pk=fs_id)

        serializer = ProjectOutputSerializer(projects, many=True)

        return Response(serializer.data)


class ProjectsByService(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, s_id):
        if not s_id:
            return Response({'error': "s_id (service id) param is missing"})

        s_check = Service.objects.filter(id=s_id)

        if not s_check.exists():
            return Response({'error': f"Service with the id {s_id} does not exist."})

        projects = Project.objects.filter(services__pk=s_id)

        serializer = ProjectOutputSerializer(projects, many=True)

        return Response(serializer.data)


class ProjectsByPerson(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, p_id):
        if not p_id:
            return Response({'error': "p_id (person id) param is missing"})

        p_check = Person.objects.filter(id=p_id)

        if not p_check.exists():
            return Response({'error': f"Person with the id {p_id} does not exist."})

        projects = Project.objects.filter(c_euco_id=p_id)

        serializer = ProjectOutputSerializer(projects, many=True)

        return Response(serializer.data)