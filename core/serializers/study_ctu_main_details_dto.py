from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from context.serializers.ctu_dto import CTUOutputSerializer
from context.serializers.person_dto import PersonOutputSerializer


class StudyCTUMainDetailsSerializer(serializers.ModelSerializer):
    ctu = CTUOutputSerializer(many=False, read_only=False)
    pi = PersonOutputSerializer(many=False, read_only=False)

    class Meta:
        model = StudyCTU
        fields = fields = ['id', 'site_number', 'patients_expected', 'recruitment_greenlight', 'mov_expected_number', 'ctu', 'pi', 'pi_national_coordinator']