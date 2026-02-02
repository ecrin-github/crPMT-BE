from rest_framework import serializers

from core.models.centre import Centre
from context.serializers.hospital_dto import HospitalOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer


class CentreMainDetailsSerializer(serializers.ModelSerializer):
    hospital = HospitalOutputSerializer(many=False, read_only=True)
    pi = PersonOutputSerializer(many=False, read_only=False)

    class Meta:
        model = Centre
        fields = [
            "id",
            "hospital",
            "site_number_flag",
            "site_number",
            "pi",
            "pi_national_coordinator",
            "patients_expected",
            "recruitment_greenlight",
            "mov_expected_number",
        ]
