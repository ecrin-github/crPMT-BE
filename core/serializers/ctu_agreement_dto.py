from rest_framework import serializers

from context.serializers.ctu_status_dto import CTUStatusOutputSerializer
from core.models.ctu_agreement import CTUAgreement
from core.serializers.ctu_agreement_amendment_dto import CTUAgreementAmendmentOutputSerializer
from core.serializers.study_ctu_main_details_dto import StudyCTUMainDetailsSerializer


class CTUAgreementInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTUAgreement
        fields = '__all__'


class CTUAgreementOutputSerializer(serializers.ModelSerializer):
    ctu_agreement_amendments = CTUAgreementAmendmentOutputSerializer(many=True, read_only=True)
    ctu_status = CTUStatusOutputSerializer(many=False, read_only=True)
    study_ctu = StudyCTUMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = CTUAgreement
        fields = '__all__'
