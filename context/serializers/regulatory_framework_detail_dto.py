from rest_framework import serializers

from context.models.regulatory_framework_detail import RegulatoryFrameworkDetail


class RegulatoryFrameworkDetailInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegulatoryFrameworkDetail
        fields = '__all__'


class RegulatoryFrameworkDetailOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegulatoryFrameworkDetail
        fields = '__all__'
