from rest_framework import serializers

from core.models.study_agreement import StudyAgreement


class StudyAgreementMainDetailsSerializer(serializers.ModelSerializer):
    fully_executed = serializers.ReadOnlyField()

    class Meta:
        model = StudyAgreement
        fields = ["id", "draft_sent_date", "signed_by_sponsor_date", "signed_by_ecrin_date",
                  "fully_executed", "start_date", "end_date", "comment"]
