from rest_framework import serializers

from context.models.organisation import Organisation
from context.serializers.country_dto import CountryOutputSerializer


class OrganisationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organisation
        fields = '__all__'


class OrganisationOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Organisation
        fields = '__all__'
