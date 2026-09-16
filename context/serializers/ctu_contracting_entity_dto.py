from rest_framework import serializers

from context.models.ctu_contracting_entity import CtuContractingEntity


class CtuContractingEntityInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CtuContractingEntity
        fields = '__all__'


class CtuContractingEntityOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CtuContractingEntity
        fields = '__all__'
