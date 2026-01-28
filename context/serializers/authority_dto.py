from rest_framework import serializers

from context.models.authority import Authority


class AuthorityInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Authority
        fields = '__all__'


class AuthorityOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Authority
        fields = '__all__'
