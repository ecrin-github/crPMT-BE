from rest_framework import serializers

from users.models.profiles import UserProfiles


class UserProfilesInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = '__all__'


class UserProfilesOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = '__all__'


class UserProfilesLimitedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfiles
        fields = ['id', 'organisation']