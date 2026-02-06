from rest_framework import serializers

from context.serializers.ctu_status_dto import CTUStatusOutputSerializer
from core.models.ctu_agreement import CTUAgreement


class CTUAgreementMainDetailsSerializer(serializers.ModelSerializer):
    ctu_status = CTUStatusOutputSerializer(many=False, read_only=True)

    class Meta:
        model = CTUAgreement
        fields = ["id", "signed", "start_date", "end_date", "ctu_status"]
