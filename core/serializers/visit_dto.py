from rest_framework import serializers

from core.models.visit import Visit
from core.serializers.centre_dto import CentreOutputSerializer


class VisitInputSerializer(serializers.ModelSerializer):
    # TODO: test type for input

    class Meta:
        model = Visit
        fields = '__all__'
    
    def get_fields(self):
        result = super().get_fields()
        visit_type = result.pop('visit_type')
        result['type'] = visit_type
        return result


class VisitOutputSerializer(serializers.ModelSerializer):
    centre = CentreOutputSerializer(many=False, read_only=True)

    class Meta:
        model = Visit
        fields = '__all__'
    
    def get_fields(self):
        result = super().get_fields()
        visit_type = result.pop('visit_type')
        result['type'] = visit_type
        return result
