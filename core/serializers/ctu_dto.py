from rest_framework import serializers

from core.models.ctu import CTU
from core.serializers.country_dto import CountryOutputSerializer
from core.serializers.person_dto import PersonOutputSerializer


class CTUInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTU
        fields = '__all__'


class CTUOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)
    contact = PersonOutputSerializer(many=False, read_only=True)

    class Meta:
        model = CTU
        fields = '__all__'
