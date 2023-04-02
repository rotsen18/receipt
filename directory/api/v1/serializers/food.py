from rest_framework import serializers

from directory.models import CookingType, CulinaryCategory, Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class CookingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookingType
        fields = '__all__'


class CulinaryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CulinaryCategory
        fields = '__all__'
