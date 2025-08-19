from rest_framework import serializers

from context.models.person import Person
from context.serializers.country_dto import CountryOutputSerializer


class PersonInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class PersonOutputSerializer(serializers.ModelSerializer):
    country = CountryOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'
