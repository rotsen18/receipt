from rest_framework import viewsets

from directory.api.v1.serializers import devices as serializers
from directory.models import Device


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = serializers.DeviceSerializer
