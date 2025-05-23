from rest_framework import serializers

from context.models.study_status import StudyStatus


class StudyStatusInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyStatus
        fields = '__all__'


class StudyStatusOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyStatus
        fields = '__all__'
