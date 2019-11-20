"""
프로그램 ID:SV-1500-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-11-13
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 주소관련 내용을 다루고 있다.
"""

from django.db import models


class SiDo(models.Model):
    siDoId = models.CharField(
        primary_key=True,
        max_length=30,
        db_column='sidoid'
    )
    siDoName = models.CharField(
        max_length=127,
        db_column='sidoname'
    )

    class Meta:
        db_table = 'Sido'


class SiGunGu(models.Model):
    siGunGuId = models.CharField(
        primary_key=True,
        max_length=30,
        db_column='sigunguid'
    )
    siGunGuName = models.CharField(
        max_length=127,
        db_column='sigunguname'
    )

    class Meta:
        db_table = 'Sigungu'


class Address(models.Model):
    addressId = models.AutoField(
        primary_key=True,
        db_column='addressid'
    )
    siDoId = models.ForeignKey(
        SiDo,
        on_delete=models.CASCADE,
        db_column='sidoid'
    )
    siGunGuId = models.OneToOneField(
        SiGunGu,
        on_delete=models.CASCADE,
        db_column='sigunguid'
    )
    siDoSiGunGuName = models.CharField(
        max_length=255,
        unique=True,
        db_column='sidosigunguname'
    )

    class Meta:
        db_table = 'Address'
