from rest_framework import serializers
from .models import Institution, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class InstitutionSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = "__all__"

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['categories'] = CategorySerializer(instance.categories).data
    #     return response
