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
