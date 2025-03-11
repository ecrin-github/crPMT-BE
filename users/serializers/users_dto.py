import logging
import string
import random

from django.core.exceptions import BadRequest
from rest_framework import serializers

# from users.models import UserProfiles
from users.models.users import Users
from users.serializers.create_user_class import CreateUserDto
# from users.serializers.profiles_dto import UserProfilesOutputSerializer, UserProfilesLimitedOutputSerializer

logger = logging.getLogger('django')


class UsersSerializer(serializers.ModelSerializer):
    # user_profile = UserProfilesOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Users
        exclude = ['password']


class UsersLimitedSerializer(serializers.ModelSerializer):
    # user_profile = UserProfilesLimitedOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Users
        fields = ['id', 'user_profile', 'email', 'first_name', 'last_name', 'ls_aai_id']


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    sub = serializers.CharField(required=False, max_length=500, allow_blank=True, default='')
    name = serializers.CharField(required=False, max_length=150, allow_blank=True, default='')
    family_name = serializers.CharField(required=False, max_length=75, allow_blank=True, default='')
    first_name = serializers.CharField(required=False, max_length=75, allow_blank=True, default='')
    last_name = serializers.CharField(required=False, max_length=75, allow_blank=True, default='')
    # prof_title = serializers.CharField(required=False, max_length=100, allow_blank=True, default='')
    # designation = serializers.CharField(required=False, max_length=100, allow_blank=True, default='')
    # organisation = serializers.CharField(required=False, max_length=150, allow_blank=True, default='')
    is_superuser = serializers.BooleanField(required=False, default=False)

    def update_user_data(self, user_data, user_dto):
        user_data.is_active = (user_dto.sub != '')
        user_data.ls_aai_id = user_dto.sub
        user_data.email = user_dto.email
        user_data.username = user_dto.email
        if user_dto.first_name or user_dto.last_name:
            user_data.first_name = user_dto.first_name
            user_data.last_name = user_dto.last_name
        else:
            user_data.first_name = user_dto.name.split(' ')[0]
            user_data.last_name = user_dto.family_name
        user_data.save()
    
    # def update_user_profile_data(self, user_profile_data, user_dto):
    #     if user_dto.organisation:
    #         organisation = Organisations.objects.get(id=user_dto.organisation)
    #         if organisation:
    #             user_profile_data.organisation = organisation  
    #     if user_dto.prof_title:   
    #         user_profile_data.prof_title = user_dto.prof_title
    #     if user_dto.designation:
    #         user_profile_data.designation = user_dto.designation
    #     user_profile_data.save()

    def create(self, validated_data):
        user_dto = CreateUserDto(**validated_data)

        # user_profile_data_check = UserProfiles.objects.filter(ls_aai_id=user_dto.sub)
        user_data_check = Users.objects.filter(ls_aai_id=user_dto.sub)
        if user_dto.sub and user_data_check.exists():
            logger.debug('user dto sub and userdatacheck')
            user_data = Users.objects.get(ls_aai_id=user_dto.sub)
            logger.debug(f'user data: {user_data}')
            self.update_user_data(user_data, user_dto)
            # user_profile_data = UserProfiles.objects.get(ls_aai_id=user_dto.sub)
            # if user_profile_data.user:
            #     # Update user data
            #     if user_profile_data.user.id:
            #         user_data = Users.objects.get(id=user_profile_data.user.id)
            #         if user_data:
            #             self.update_user_data(user_data, user_dto)
            # else:
            #     raise BadRequest()
            # self.update_user_profile_data(user_profile_data, user_dto)
        else:
            user_check_email = Users.objects.filter(email=user_dto.email)
            if user_check_email.exists():
                # Update user data
                user_data = Users.objects.get(email=user_dto.email)
                self.update_user_data(user_data, user_dto)
            else:
                # Create user
                user_data = Users(username=user_dto.email)
                password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
                user_data.set_password(password)
                self.update_user_data(user_data, user_dto)

            # Test to see if user profile exists and was created with user interface without ls aai id
            # user_profile_data_check = UserProfiles.objects.filter(user=user_data.id)
            # if user_profile_data_check.exists():
            #     user_profile_data = UserProfiles.objects.get(user=user_data.id)
            #     user_profile_data.ls_aai_id = user_dto.sub
            # else:
            #     # Create user profile with user id
            #     user_profile_data = UserProfiles(user=user_data, ls_aai_id=user_dto.sub)
            # self.update_user_profile_data(user_profile_data, user_dto)
        return user_data

    def update(self, instance, validated_data):
        instance.save()
        return instance
