from rest_framework import serializers

from core.models.centre import Centre
from context.serializers.person_dto import PersonOutputSerializer
from core.serializers.study_ctu_main_details_dto import StudyCTUMainDetailsSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer


class CentreInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Centre
        fields = '__all__'


class CentreOutputSerializer(serializers.ModelSerializer):
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_ctu = StudyCTUMainDetailsSerializer(many=False, read_only=True)
    pi = PersonOutputSerializer(many=False, read_only=False)

    class Meta:
        model = Centre
        fields = '__all__'