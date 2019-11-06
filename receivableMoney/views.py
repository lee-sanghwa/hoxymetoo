"""
프로그램 ID:SV-1420-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-17
버전:0.5
설명:
- 회원이 받을 수 있는 수혜 가능 금액과 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
"""

from receivableMoney.serializers import MemberReceivableMoneySerializer
from receivableMoney.models import MemberReceivableMoney
from hoxymetoo.create_log import create_log_content
from rest_framework import viewsets
import logging

logger = logging.getLogger(__name__)


class MemberReceivableMoneyViewSet(viewsets.ModelViewSet):
    queryset = MemberReceivableMoney.objects.all()
    serializer_class = MemberReceivableMoneySerializer

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
