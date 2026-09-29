from rest_framework import serializers

from context.models.ecrin_contracting_entity import EcrinContractingEntity


class EcrinContractingEntityInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = EcrinContractingEntity
        fields = '__all__'


class EcrinContractingEntityOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = EcrinContractingEntity
        fields = '__all__'
