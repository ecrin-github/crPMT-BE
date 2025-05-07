from rest_framework import serializers

from core.models.reporting_period import ReportingPeriod


class ReportingPeriodInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportingPeriod
        fields = '__all__'


class ReportingPeriodOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportingPeriod
        fields = '__all__'
