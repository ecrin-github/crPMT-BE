from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from context.serializers.ctu_dto import CTUOutputSerializer


class StudyCTUMainDetailsSerializer(serializers.ModelSerializer):
    ctu = CTUOutputSerializer(many=False, read_only=False)

    class Meta:
        model = StudyCTU
        fields = fields = ['id', 'ctu']