from django.shortcuts import get_object_or_404
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from context.models.complex_trial_type import ComplexTrialType
from context.models.ctu import CTU
from context.models.funding_source import FundingSource
from context.models.organisation import Organisation
from context.models.person import Person
from context.models.service import Service
from core.serializers.centre_dto import *
from core.serializers.project_dto import *
from core.serializers.study_dto import *
from core.serializers.study_country_dto import *
from core.serializers.study_ctu_dto import *
from core.serializers.visit_dto import *
from core.models.centre import Centre
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
            return StudyCTU.objects.none()
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


class CentreView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    queryset = Centre.objects.all()
    object_class = Centre
    serializer_class = CentreOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CentreInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Centre.objects.none()
        if 'sctuId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_ctu=self.kwargs['sctuId'])
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
                .filter(centre=self.kwargs['sId'])
            )
        if 'sctuId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(centre=self.kwargs['sctuId'])
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


class ProjectsByOrganisation(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, org_id):
        if not org_id:
            return Response({'error': "org_id (organisation id) param is missing"})

        p_check = Organisation.objects.filter(id=org_id)

        if not p_check.exists():
            return Response({'error': f"Organisation with the id {org_id} does not exist."})

        projects = Project.objects.filter(coordinator=org_id)

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


class ReferenceCountByClass(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication, OIDCAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, class_name, obj_id):
        if not obj_id:
            return Response({'error': "id param is missing"})
        if not class_name:
            return Response({'error': "class param is missing"})

        obj = None
        class_name = class_name.lower()

        if class_name == "complextrialtype":
            obj = get_object_or_404(ComplexTrialType, pk=obj_id)
        elif class_name == "fundingsource":
            obj = get_object_or_404(FundingSource, pk=obj_id)
        elif class_name == "organisation":
            obj = get_object_or_404(Organisation, pk=obj_id)
        elif class_name == "person":
            obj = get_object_or_404(Person, pk=obj_id)
        elif class_name == "service":
            obj = get_object_or_404(Service, pk=obj_id)

        if obj is None:
            return Response({'error': f"unknown class {class_name}"}) 

        total_count = 0
        response = {}
        # https://stackoverflow.com/a/54711672
        # reverse relation "fields" on the Reporter model are auto-created and not concrete
        for reverse in [f for f in obj._meta.get_fields() if f.auto_created and not f.concrete]:
            name = reverse.get_accessor_name()
            count = getattr(obj, name).count()
            response[name] = count
            total_count += count

        response["total_count"] = total_count
        return Response(response)