from rest_framework import serializers

from core.models.publication import Publication


class PublicationInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = '__all__'


class PublicationOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publication
        fields = '__all__'
