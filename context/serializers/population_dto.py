from rest_framework import serializers

from context.models.population import Population


class PopulationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Population
        fields = '__all__'


class PopulationOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Population
        fields = '__all__'
