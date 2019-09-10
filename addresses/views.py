from addresses.models import SiDo, SiGunGu, Address
from addresses.serializers import SiDoSerializer, SiGunGuSerializer, AddressSerializer
from rest_framework import viewsets


class SiDoViewSet(viewsets.ModelViewSet):
    queryset = SiDo.objects.all()
    serializer_class = SiDoSerializer


class SiGunGuViewSet(viewsets.ModelViewSet):
    queryset = SiGunGu.objects.all()
    serializer_class = SiGunGuSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
