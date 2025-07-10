from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from context.serializers.ctu_dto import CTUOutputSerializer
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer
from core.serializers.centre_dto import CentreOutputSerializer


class StudyCTUInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudyCTU
        fields = '__all__'


class StudyCTUOutputSerializer(serializers.ModelSerializer):
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_country = StudyCountryMainDetailsSerializer(many=False, read_only=True)
    ctu = CTUOutputSerializer(many=False, read_only=False)
    centres = CentreOutputSerializer(many=True)

    class Meta:
        model = StudyCTU
        fields = '__all__'