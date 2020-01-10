"""
프로그램 ID:SV-1520-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-11-13
버전:0.5
설명:
- 주소와 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
- 시,도 와 시,군,구에 대한 정보를 반환해준다.
"""

from addresses.models import SiDo, SiGunGu, Address
from addresses.serializers import SiDoSerializer, SiGunGuSerializer, AddressSerializer
from hoxymetoo.create_log import create_log_content
from rest_framework.mixins import ListModelMixin
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)


class SiDoViewSet(viewsets.ModelViewSet):
    queryset = SiDo.objects.all().order_by('siDoName')
    serializer_class = SiDoSerializer

    def list(self, request, *args, **kwargs):
        logger.info("TRY LIST SI DO  ||" + create_log_content(request))
        return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("TRY CREATE SI DO  ||" + create_log_content(request))
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("TRY RETRIEVE SI DO  ||" + create_log_content(request))
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("TRY UPDATE SI DO  ||" + create_log_content(request))
        return super().update(self, request, *args, **kwargs)


class SiGunGuViewSet(viewsets.ModelViewSet):
    queryset = SiGunGu.objects.all().order_by('siGunGuName')
    serializer_class = SiGunGuSerializer

    def list(self, request, *args, **kwargs):
        logger.info("TRY LIST SI GUN GU  ||" + create_log_content(request))
        existing_queryset = self.queryset
        query_dict = request.GET

        si_do_id = query_dict.get('sidoid')

        if si_do_id is not None:
            select_si_gun_gu_with_si_do_query = """
            SELECT * FROM Sigungu
            JOIN Address ON Sigungu.sigunguid = Address.sigunguid
            WHERE Address.sidoid = (%s)
            AND Sigungu.siGunGuId != (%s)
            ORDER BY siGunGuName
            """

            bon_cheung_id = '9999999'
            select_si_gun_gu_with_si_do_query = select_si_gun_gu_with_si_do_query % (si_do_id, bon_cheung_id)
            existing_queryset = SiGunGu.objects.raw(select_si_gun_gu_with_si_do_query)

        self.queryset = existing_queryset

        return ListModelMixin.list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("TRY CREATE SI GUN GU  ||" + create_log_content(request))
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("TRY RETRIEVE SI GUN GU  ||" + create_log_content(request))
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("TRY UPDATE SI GUN GU  ||" + create_log_content(request))
        return super().update(self, request, *args, **kwargs)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by('siDoSiGunGuName')
    serializer_class = AddressSerializer

    def list(self, request, *args, **kwargs):
        logger.info("TRY LIST ADDRESS  ||" + create_log_content(request))
        return super().list(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info("TRY CREATE ADDRESS  ||" + create_log_content(request))
        return super().create(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("TRY RETRIEVE ADDRESS  ||" + create_log_content(request))
        return super().retrieve(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info("TRY UPDATE ADDRESS  ||" + create_log_content(request))
        return super().update(self, request, *args, **kwargs)
