from rest_framework import serializers

from context.models.visit_type import VisitType
from core.serializers.centre_main_details_dto import CentreMainDetailsSerializer


class VisitTypeInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitType
        fields = '__all__'


class VisitTypeOutputSerializer(serializers.ModelSerializer):
    centre = CentreMainDetailsSerializer(many=False)

    class Meta:
        model = VisitType
        fields = '__all__'
