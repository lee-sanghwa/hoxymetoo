from .models import Welfare
from .serializers import WelfareSerializer
from rest_framework import viewsets


class WelfareViewSet(viewsets.ModelViewSet):
    queryset = Welfare.objects.all()
    serializer_class = WelfareSerializer
