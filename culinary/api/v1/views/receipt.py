from rest_framework import viewsets, mixins

from culinary.models import Receipt, ReceiptComponent, ReceiptComment
from culinary.api.v1.serializers import receipt as serializers


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ReceiptListSerializer
        elif self.action == 'retrieve':
            return serializers.ReceiptDetailSerializer
        return serializers.ReceiptSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReceiptComponentViewSet(viewsets.ModelViewSet):
    queryset = ReceiptComponent.objects.all()
    serializer_class = serializers.ReceiptComponentSerializer

    def perform_create(self, serializer):
        serializer.save(receipt_id=self.kwargs.get('receipt_pk'), author=self.request.user)


class ReceiptCommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ReceiptComment.objects.all()
    serializer_class = serializers.ReceiptCommentSerializer

    def perform_create(self, serializer):
        serializer.save(receipt_id=self.kwargs.get('receipt_pk'), author=self.request.user)
