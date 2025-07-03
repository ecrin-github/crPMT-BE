from rest_framework import serializers

from context.models.service import Service


class ServiceInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class ServiceOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
