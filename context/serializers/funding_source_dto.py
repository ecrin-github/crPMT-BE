from rest_framework import serializers

from context.models.funding_source import FundingSource


class FundingSourceInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundingSource
        fields = '__all__'


class FundingSourceOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FundingSource
        fields = '__all__'
