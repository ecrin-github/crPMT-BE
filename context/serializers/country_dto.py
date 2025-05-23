from rest_framework import serializers

from context.models.country import Country


class CountryInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class CountryOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
