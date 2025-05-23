from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from context.serializers.ctu_dto import CTUOutputSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer


class StudyCTUInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyCTU
        fields = '__all__'


class StudyCTUOutputSerializer(serializers.ModelSerializer):
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    ctu = CTUOutputSerializer(many=False, read_only=False)

    class Meta:
        model = StudyCTU
        fields = '__all__'
