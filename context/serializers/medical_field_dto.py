from rest_framework import serializers

from context.models.medical_field import MedicalField


class MedicalFieldInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalField
        fields = '__all__'


class MedicalFieldOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicalField
        fields = '__all__'
