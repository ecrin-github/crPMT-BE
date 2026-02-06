from rest_framework import serializers

from core.models.visit import Visit
from core.serializers.centre_main_details_dto import CentreMainDetailsSerializer


class VisitInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = '__all__'


class VisitOutputSerializer(serializers.ModelSerializer):
    centre = CentreMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'
