from rest_framework import serializers

from context.models.ctu_status import CTUStatus


class CTUStatusInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTUStatus
        fields = '__all__'


class CTUStatusOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTUStatus
        fields = '__all__'
