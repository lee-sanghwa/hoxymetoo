from django.db import models


class Trgterindvdlarray(models.Model):
    # 가구유형 id ( 001 ~ 007 )
    trgterindvdlid = models.IntegerField(unique=True)
    # 가구유형 ( 해당없음, 한부모, 다문화, 조손, 새터민,소년소녀가장, 독거노인 )
    trgterindvdlname = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'Trgterindvdlarray'


class Obstlvarray(models.Model):
    obstlvid = models.IntegerField(unique=True)
    obstlvname = models.CharField(max_length=7, unique=True)

    class Meta:
        db_table = 'Obstlvarray'


class Obstkiarray(models.Model):
    obstkiid = models.IntegerField(unique=True)
    obstkiunqid = models.CharField(max_length=2, unique=True)
    obstkiname = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'Obstkiarray'


class Disable(models.Model):
    obstlvid = models.ForeignKey(Obstlvarray)
    obstkiid = models.ForeignKey(Obstkiarray)

    class Meta:
        db_table = 'Disable'


class Desirearray(models.Model):
    desireid = models.IntegerField(unique=True)
    desireunqid = models.CharField(max_length=2, unique=True)
    desirename = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Desirearray'


class Chartrgterarray(models.Model):
    chartrgterid = models.IntegerField(unique=True)
    chartrgtername = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Chartrgterarray'


class Lifearray(models.Model):
    lifeid = models.IntegerField(unique=True)
    lifename = models.CharField(max_length=7, unique=True)

    class Meta:
        db_table = 'Lifearray'

class Jurmnof(models.Model):
    jurmnofid = models.IntegerField(unique=True)
    jurmnofname = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Jurmnof'


class Jurorg(models.Model):
    jurorgid = models.IntegerField(unique=True)
    jurorgname = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Jurorg'


class Welfare(models.Model):
    welid = models.IntegerField(unique=True)
    serviceid = models.CharField(max_length=63, unique=True)
    servicename = models.CharField(max_length=127)
    servicesummary = models.CharField(max_length=255)
    targetdetail = models.CharField(max_length=511)
    supportstandard = models.CharField(max_length=511)
    supportmoney = models.CharField(max_length=511)
    servicedetail = models.CharField(max_length=65535)
    servicedetailimage = models.CharField(max_length=511)
    contactinfoname = models.CharField(max_length=127)
    contactinfonumber = models.CharField(max_length=31)
    sitename = models.CharField(max_length=63)
    sitelink = models.CharField(max_length=255)
    formname = models.CharField(max_length=63)
    formlink = models.CharField(max_length=255)
    lawname = models.CharField(max_length=63)
    lawlink = models.CharField(max_length=255)
    registerdate = models.CharField(max_length=100)
    housetypes = models.ManyToManyField(
        Trgterindvdlarray,
        through='Weltrgterindvdl'
    )
    disables = models.ManyToManyField(
        Disable,
        through='Weldisable'
    )
    desires = models.ManyToManyField(
        Desirearray,
        through='Weldesire'
    )
    targetcharacters = models.ManyToManyField(
        Chartrgterarray,
        through='Welchartrgter'
    )
    lifetimes = models.ManyToManyField(
        Lifearray,
        through='Wellife'
    )
    departments = models.ManyToManyField(
        Jurmnof,
        through='Weljurmnof'
    )
    organizations = models.ManyToManyField(
        Jurorg,
        through='Weljurorg'
    )

    class Meta:
        db_table = 'Welfare'


class Weltrgterindvdl(models.Model):
    welid = models.ForeignKey(Welfare)
    trgterindvdlid = models.ForeignKey(Trgterindvdlarray)

    class Meta:
        db_table = 'Weltrgterindvdl'


class Weldesire(models.Model):
    welid = models.ForeignKey(Welfare)
    desireid = models.ForeignKey(Desirearray)

    class Meta:
        db_table = 'Weldesire'


class Weldisable(models.Model):
    welid = models.ForeignKey(Welfare)
    disableid = models.ForeignKey(Disable)

    class Meta:
        db_table = 'Weldisable'


class Welchartrgter(models.Model):
    welid = models.ForeignKey(Welfare)
    chartrgterid = models.ForeignKey(Chartrgterarray)

    class Meta:
        db_table = 'Welchartrgter'


class Wellife(models.Model):
    welid = models.ForeignKey(Welfare)
    lifeid = models.ForeignKey(Lifearray)

    class Meta:
        db_table = 'Wellife'


class Weljurmnof(models.Model):
    welid = models.ForeignKey(Welfare)
    jurmnofid = models.ForeignKey(Jurmnof)

    class Meta:
        db_table = 'Weljurmnof'

class Weljurorg(models.Model):
    welid = models.ForeignKey(Welfare)
    jurorg = models.ForeignKey(Jurorg)

    class Meta:
        db_table = 'Weljurorg'


