from rest_framework import serializers

from core.models.study_agreement import StudyAgreement
from core.serializers.study_agreement_amendment_dto import StudyAgreementAmendmentOutputSerializer


class StudyAgreementInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyAgreement
        fields = '__all__'


class StudyAgreementOutputSerializer(serializers.ModelSerializer):
    study_agreement_amendments = StudyAgreementAmendmentOutputSerializer(many=True, read_only=True)
    fully_executed = serializers.ReadOnlyField()

    class Meta:
        model = StudyAgreement
        fields = '__all__'
