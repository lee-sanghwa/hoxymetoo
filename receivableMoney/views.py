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
from rest_framework import viewsets


class MemberReceivableMoneyViewSet(viewsets.ModelViewSet):
    queryset = MemberReceivableMoney.objects.all()
    serializer_class = MemberReceivableMoneySerializer
