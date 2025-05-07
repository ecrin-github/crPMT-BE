from rest_framework import serializers

from core.models.country import Country


class CountryInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class CountryOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
