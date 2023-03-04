from django.urls import path
from rest_framework_nested import routers

from culinary.api.v1.views.receipt import ReceiptViewSet, ReceiptComponentViewSet, ReceiptCommentViewSet

router = routers.SimpleRouter()
router.register(r'receipt', ReceiptViewSet, basename='receipt')

receipt_router = routers.NestedSimpleRouter(router, r'receipt', lookup='receipt')
receipt_router.register('comment', ReceiptCommentViewSet)
receipt_router.register('component', ReceiptComponentViewSet)

urlpatterns = [
]

urlpatterns += router.urls
urlpatterns += receipt_router.urls
