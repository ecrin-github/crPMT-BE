from rest_framework import serializers

from core.models.satisfaction_survey import SatisfactionSurvey


class SatisfactionSurveyInputSerializer(serializers.ModelSerializer):
    # A survey is always sent to at least 1 person
    number_of_recipients = serializers.IntegerField(min_value=1, required=False, allow_null=True)

    class Meta:
        model = SatisfactionSurvey
        fields = '__all__'


class SatisfactionSurveyOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = SatisfactionSurvey
        fields = '__all__'
