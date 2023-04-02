from rest_framework import routers

from directory.api.v1.views.device import DeviceViewSet
from directory.api.v1.views.food import CookingTypeViewSet, CulinaryCategoryViewSet, IngredientViewSet

router = routers.SimpleRouter()
router.register(r'device', DeviceViewSet, basename='device')
router.register(r'ingredient', IngredientViewSet, basename='ingredient')
router.register(r'cooking_type', CookingTypeViewSet, basename='cooking_type')
router.register(r'culinary_category', CulinaryCategoryViewSet, basename='culinary_category')

urlpatterns = [
]

urlpatterns += router.urls
