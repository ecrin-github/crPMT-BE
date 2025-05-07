from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer
from core.serializers.ctu_dto import CTUOutputSerializer


class StudyCTUInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyCTU
        fields = '__all__'


class StudyCTUOutputSerializer(serializers.ModelSerializer):
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    ctu = CTUOutputSerializer(many=False, read_only=True)

    class Meta:
        model = StudyCTU
        fields = '__all__'
