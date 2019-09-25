from addresses.models import SiDo, SiGunGu, Address
from addresses.serializers import SiDoSerializer, SiGunGuSerializer, AddressSerializer
from rest_framework.mixins import ListModelMixin
from rest_framework import viewsets


class SiDoViewSet(viewsets.ModelViewSet):
    queryset = SiDo.objects.all()
    serializer_class = SiDoSerializer


class SiGunGuViewSet(viewsets.ModelViewSet):
    queryset = SiGunGu.objects.all()
    serializer_class = SiGunGuSerializer

    def list(self, request, *args, **kwargs):
        existing_queryset = self.queryset
        query_dict = request.GET

        si_do_id = query_dict.get('sidoid')

        if si_do_id is not None:
            select_si_gun_gu_with_si_do_query = """
            SELECT * FROM Sigungu
            JOIN Address ON Sigungu.sigunguid = Address.sigunguid
            WHERE Address.sidoid = (%s)
            AND Sigungu.siGunGuId != (%s)
            """
            bon_cheung_id = '9999999'
            select_si_gun_gu_with_si_do_query = select_si_gun_gu_with_si_do_query % (si_do_id, bon_cheung_id)
            existing_queryset = SiGunGu.objects.raw(select_si_gun_gu_with_si_do_query)

        self.queryset = existing_queryset

        return ListModelMixin.list(self, request, *args, **kwargs)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
