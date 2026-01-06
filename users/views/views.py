import datetime

from django.db.models import Value, Q
from django.db.models.functions import Concat
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from app.permissions import IsSuperUser, WriteOnlyForSelf
# from mdm.models import Studies, DataObjects, ObjectInstances
# from rms.models import DataUseProcesses, DataTransferProcesses, DupStudies, DupObjects, DtpStudies, DtpObjects, DtpPeople, DupPeople
# from users.models.profiles import UserProfiles
from users.models.users import Users
# from users.serializers.profiles_dto import UserProfilesOutputSerializer, UserProfilesInputSerializer
from users.serializers.users_dto import UsersSerializer, CreateUserSerializer, UsersLimitedSerializer


class UsersList(GenericAPIView):
    queryset = Users.objects.filter(~Q(username='tsd'))
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = None
        if "sub" in request.GET:
            user_check = self.get_queryset(*args, **kwargs).filter(ls_aai_id=sub)
            if user_check.exists():
                sub = request.GET['sub']
                user = self.get_queryset(*args, **kwargs).get(ls_aai_id=sub)
            # user_profile_check = UserProfiles.objects.filter(ls_aai_id=sub)
            # if user_profile_check.exists():
            #     user_profile = UserProfiles.objects.get(ls_aai_id=sub)
            #     user_check = self.get_queryset(*args, **kwargs).filter(id=user_profile.user.id)
            #     if user_check.exists():
            #         user = self.get_queryset(*args, **kwargs).get(id=user_profile.user.id)
            #         serializer = UsersSerializer(user, many=False)
        elif request.user.id:
            users = []
            if request.user.is_superuser:
                users = self.get_queryset(*args, **kwargs)
                serializer = UsersLimitedSerializer(users, many=True)
                serializer = UsersLimitedSerializer(users, many=True)
                serializer = UsersSerializer(users, many=True)
            # else:
                # try:
                #     # Unused
                #     users_subquery = self.get_queryset(*args, **kwargs).raw("SELECT u.id as id FROM users u LEFT JOIN "
                #                         + "user_profiles up ON u.id=up.user_id "
                #                         + f"WHERE up.organisation_id='{request.user.user_profile.organisation.id}';")
                #     for user in users_subquery:
                #         users.append(user)
                # except AttributeError:
                #     return Response(status=404, data='Error: no organisation for user')
                # serializer = UsersLimitedSerializer(users, many=True)

        if not serializer:
            return Response(status=404, data="Requested user not found")
        return Response({'count': len(serializer.data), 'results': serializer.data, 'statusCode': status.HTTP_200_OK})


class UserView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated & (WriteOnlyForSelf | IsSuperUser)]

    def get_serializer_class(self):
        if self.action in ["create"]:
            return CreateUserSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        self.perform_create(input_serializer)

        user = Users.objects.get(email=input_serializer.validated_data["email"])
        output_serializer = UsersSerializer(user)
        return Response(output_serializer.data)

    def perform_create(self, serializer):
        serializer.save()


# class UserProfilesList(viewsets.ModelViewSet):
#     queryset = UserProfiles.objects.all()
#     serializer_class = UserProfilesOutputSerializer
#     permission_classes = [permissions.IsAuthenticated & (WriteOnlyForSelf | IsSuperUser)]

#     def get_serializer_class(self):
#         if self.action in ["create", "update", "partial_update"]:
#             return UserProfilesInputSerializer
#         return super().get_serializer_class()

#     def get_queryset(self, *args, **kwargs):
#         return (
#             super()
#             .get_queryset(*args, **kwargs)
#             .filter(user=self.kwargs['userId'])
#         )


class UsersByName(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request):
        name = self.request.query_params.get('name')

        if name is None:
            return Response({'error': "name param is missing"})

        queryset = Users.objects.annotate(fullname=Concat('first_name', Value(' '), 'last_name'))
        result = queryset.filter(Q(fullname__icontains=name) | Q(email__icontains=name))

        serializer = UsersSerializer(result, many=True)

        return Response({'count': result.count(), 'results': serializer.data, 'statusCode': status.HTTP_200_OK})


# class UserByEmail(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         email = self.request.query_params.get('email')

#         if email is None:
#             return Response({'error': "email param is missing"})

#         user_check = Users.objects.filter(email=email)
#         if not user_check.exists():
#             return Response({'error': f'User with the Email {email} does not exist'})

#         user_data = Users.objects.get(email=email)

#         serializer = UsersSerializer(user_data)

#         return Response(serializer.data)


# class UserByLsAaiId(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         ls_aai_id = self.request.query_params.get('id')

#         if ls_aai_id is None:
#             return Response({'error': "id param is missing"})

#         user_check = UserProfiles.objects.filter(ls_aai_id=ls_aai_id)
#         if not user_check.exists():
#             return Response({'error': f'User with the LS AAI Id {ls_aai_id} does not exist'})

#         user_profile = UserProfiles.objects.get(ls_aai_id=ls_aai_id)
#         user_data = Users.objects.get(id=user_profile.user.id)

#         serializer = UsersSerializer(user_data)

#         return Response(serializer.data)


# class UsersToNotify(APIView):
#     permission_classes = [IsSuperUser]

#     def get(self, request, sd_oid):
#         do_check = DataObjects.objects.filter(sd_oid=sd_oid)

#         if not do_check.exists():
#              return Response(status=404, data="Data Object not found")
#         else:
#             do = DataObjects.objects.get(sd_oid=sd_oid)
#             # Get DTPs where DO is linked as associated object (should be only 1 in practice)
#             dtp_ids = list(DtpObjects.objects.filter(data_object=do).values_list('dtp_id', flat=True))
#             # Get DTP associated people
#             dtp_users = list(DtpPeople.objects.filter(dtp_id__in=dtp_ids).values_list('person_id', flat=True))
#             # Get users only and not people
#             users_to_notify = list(UserProfiles.objects.filter(user_id__in=dtp_users).filter(~Q(ls_aai_id='')).values_list('user_id', flat=True))

#             return Response({"user_ids": users_to_notify}, status=200)