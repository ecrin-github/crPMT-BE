from rest_framework import serializers

from core.models.study_agreement_amendment import StudyAgreementAmendment
from core.serializers.study_agreement_main_details_dto import StudyAgreementMainDetailsSerializer


class StudyAgreementAmendmentInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyAgreementAmendment
        fields = '__all__'


class StudyAgreementAmendmentOutputSerializer(serializers.ModelSerializer):
    study_agreement = StudyAgreementMainDetailsSerializer(many=False, read_only=True)

    class Meta:
        model = StudyAgreementAmendment
        fields = '__all__'
