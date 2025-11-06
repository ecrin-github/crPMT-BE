from rest_framework import serializers

from context.models.hospital import Hospital
from context.serializers.country_dto import CountryOutputSerializer


class HospitalInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hospital
        fields = '__all__'


class HospitalOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Hospital
        fields = '__all__'
