from rest_framework import serializers

from context.models.person import Person


class PersonInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class PersonOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'
