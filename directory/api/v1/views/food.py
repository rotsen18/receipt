from rest_framework import viewsets

from directory.api.v1.serializers import food as serializers
from directory.models import CookingType, CulinaryCategory, Ingredient


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class CookingTypeViewSet(viewsets.ModelViewSet):
    queryset = CookingType.objects.all()
    serializer_class = serializers.CookingTypeSerializer


class CulinaryCategoryViewSet(viewsets.ModelViewSet):
    queryset = CulinaryCategory.objects.all()
    serializer_class = serializers.CulinaryCategorySerializer
