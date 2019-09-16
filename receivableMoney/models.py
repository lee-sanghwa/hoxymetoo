"""
프로그램 ID:SV-1400-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-17
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 회원이 받을 수 있는 금액의 내용을 다루고 있다.
"""

from django.db import models
from members.models import Member


# 데이터베이스의 회원과 수혜가능한 금액의 테이블을 연결한 테이블과 연동하기 위한 클래스
class MemberReceivableMoney(models.Model):
    socialId = models.OneToOneField(
        Member,
        to_field='memKey',
        primary_key=True,
        on_delete=models.CASCADE,
        db_column='socialid'
    )
    money1 = models.IntegerField(
        null=True,
        db_column='money1'
    )
    money2 = models.IntegerField(
        null=True,
        db_column='money2'
    )
    money3 = models.IntegerField(
        null=True,
        db_column='money3'
    )
    money4 = models.IntegerField(
        null=True,
        db_column='money4'
    )
    money5 = models.IntegerField(
        null=True,
        db_column='money5'
    )

    class Meta:
        db_table = 'Memberreceivablemoney'
