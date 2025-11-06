from rest_framework import serializers

from core.models.study_ctu import StudyCTU
from context.models.service import Service
from context.serializers.ctu_dto import CTUOutputSerializer
from context.serializers.service_dto import ServiceOutputSerializer
from core.serializers.study_country_main_details_dto import StudyCountryMainDetailsSerializer
from core.serializers.study_main_details_dto import StudyMainDetailsSerializer
from core.serializers.centre_dto import CentreOutputSerializer


class StudyCTUInputSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Service.objects.all())

    class Meta:
        model = StudyCTU
        fields = '__all__'


class StudyCTUOutputSerializer(serializers.ModelSerializer):
    services = ServiceOutputSerializer(many=True)
    study = StudyMainDetailsSerializer(many=False, read_only=True)
    study_country = StudyCountryMainDetailsSerializer(many=False, read_only=True)
    ctu = CTUOutputSerializer(many=False, read_only=False)
    centres = CentreOutputSerializer(many=True)

    class Meta:
        model = StudyCTU
        fields = '__all__'