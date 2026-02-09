from rest_framework import serializers

from core.models.ctu_agreement_amendment import CTUAgreementAmendment
from core.serializers.ctu_agreement_main_details_dto import CTUAgreementMainDetailsSerializer


class CTUAgreementAmendmentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = CTUAgreementAmendment
        fields = '__all__'


class CTUAgreementAmendmentOutputSerializer(serializers.ModelSerializer):
    ctu_agreement = CTUAgreementMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = CTUAgreementAmendment
        fields = '__all__'
