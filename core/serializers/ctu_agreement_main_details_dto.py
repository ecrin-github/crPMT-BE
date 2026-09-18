from rest_framework import serializers

from context.serializers.ctu_status_dto import CTUStatusOutputSerializer
from core.models.ctu_agreement import CTUAgreement


class CTUAgreementMainDetailsSerializer(serializers.ModelSerializer):
    ctu_status = CTUStatusOutputSerializer(many=False, read_only=True)
    fully_executed = serializers.ReadOnlyField()

    class Meta:
        model = CTUAgreement
        fields = ["id", "signed", "draft_sent_date", "signed_by_ctu_date", "signed_by_ecrin_date",
                  "fully_executed", "start_date", "end_date", "comment", "ctu_status"]
