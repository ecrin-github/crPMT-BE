from rest_framework import serializers

from context.models.complex_trial_type import ComplexTrialType


class ComplexTrialTypeInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexTrialType
        fields = '__all__'


class ComplexTrialTypeOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplexTrialType
        fields = '__all__'
