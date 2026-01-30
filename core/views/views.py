from django.shortcuts import get_object_or_404
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from context.models.complex_trial_type import ComplexTrialType
from context.models.ctu import CTU
from context.models.funding_source import FundingSource
from context.models.hospital import Hospital
from context.models.organisation import Organisation
from context.models.person import Person
from context.models.service import Service
from core.serializers.centre_dto import *
from core.serializers.notification_dto import *
from core.serializers.project_dto import *
from core.serializers.reporting_period_dto import *
from core.serializers.safety_notification_dto import *
from core.serializers.study_dto import *
from core.serializers.study_country_dto import *
from core.serializers.study_ctu_dto import *
from core.serializers.submission_dto import *
from core.serializers.visit_dto import *
from core.models.centre import *
from core.models.notification import *
from core.models.project import *
from core.models.reporting_period import *
from core.models.safety_notification import *
from core.models.study import *
from core.models.study_country import *
from core.models.study_ctu import *
from core.models.submission import *
from core.models.visit import *


class ProjectView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    object_class = Project
    serializer_class = ProjectOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProjectInputSerializer
        return super().get_serializer_class()


class StudyView(viewsets.ModelViewSet):
    queryset = Study.objects.all()
    object_class = Study
    serializer_class = StudyOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return StudyInputSerializer
        return super().get_serializer_class()


class StudyCountryView(viewsets.ModelViewSet):
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


class ReportingPeriodView(viewsets.ModelViewSet):
    queryset = ReportingPeriod.objects.all()
    object_class = ReportingPeriod
    serializer_class = ReportingPeriodOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ReportingPeriodInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return object_class.objects.none()
        if 'projectId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(project=self.kwargs['projectId'])
            )
        return super().get_queryset(*args, **kwargs)


class NotificationView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    object_class = Notification
    serializer_class = NotificationOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return NotificationInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Notification.objects.none()
        if 'scId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_country=self.kwargs['scId'])
            )
        return super().get_queryset(*args, **kwargs)


class SafetyNotificationView(viewsets.ModelViewSet):
    queryset = SafetyNotification.objects.all()
    object_class = SafetyNotification
    serializer_class = SafetyNotificationOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SafetyNotificationInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return SafetyNotification.objects.none()
        return super().get_queryset(*args, **kwargs)


class SubmissionView(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    object_class = Submission
    serializer_class = SubmissionOutputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SubmissionInputSerializer
        return super().get_serializer_class()
    
    def get_queryset(self, *args, **kwargs):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return Submission.objects.none()
        if 'scId' in self.kwargs:
            return (
                super()
                .get_queryset(*args, **kwargs)
                .filter(study_country=self.kwargs['scId'])
            )
        return super().get_queryset(*args, **kwargs)

class VisitView(viewsets.ModelViewSet):
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
        elif class_name == "ctu":
            obj = get_object_or_404(CTU, pk=obj_id)
        elif class_name == "fundingsource":
            obj = get_object_or_404(FundingSource, pk=obj_id)
        elif class_name == "hospital":
            obj = get_object_or_404(Hospital, pk=obj_id)
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
        for reverse in [f for f in obj._meta.get_fields() if f.auto_created and not f.concrete]:
            name = reverse.get_accessor_name()
            count = getattr(obj, name).count()
            response[name] = count
            total_count += count

        response["total_count"] = total_count
        return Response(response)