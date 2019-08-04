from django.db import models


class Trgterindvdlarray(models.Model):
    # 가구유형 id ( 001 ~ 007 )
    trgterindvdlid = models.IntegerField(unique=True)
    # 가구유형 ( 해당없음, 한부모, 다문화, 조손, 새터민,소년소녀가장, 독거노인 )
    trgterindvdlname = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'Trgterindvdlarray'


class Obstlvarray(models.Model):
    obstlvname = models.CharField(max_length=7, unique=True)

    class Meta:
        db_table = 'Obstlvarray'


class Obstkiarray(models.Model):
    obstkiid = models.CharField(max_length=2, unique=True)
    obstkiname = models.CharField(max_length=15, unique=True)

    class Meta:
        db_table = 'Obstkiarray'


class Disable(models.Model):
    obstlvid = models.ForeignKey(
        Obstlvarray,
        on_delete=models.CASCADE,
        db_column='obstlvid'
    )
    obstkiid = models.ForeignKey(
        Obstkiarray,
        on_delete=models.CASCADE,
        db_column='obstkiid'
    )
    disablename = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Disable'


class Desirearray(models.Model):
    desireid = models.CharField(max_length=2, unique=True)
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
    jurmnofname = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Jurmnof'


class Jurorg(models.Model):
    jurorgname = models.CharField(max_length=31, unique=True)

    class Meta:
        db_table = 'Jurorg'


class Responsible(models.Model):
    jurorgid = models.ForeignKey(
        Jurorg,
        on_delete=models.CASCADE,
        db_column='jurorgid'
    )
    jurmnofid = models.ForeignKey(
        Jurmnof,
        on_delete=models.CASCADE,
        db_column='jurmnofid'
    )
    responsiblename = models.CharField(max_length=63, unique=True)

    class Meta:
        db_table = 'Responsible'


class Welfare(models.Model):
    serviceid = models.CharField(max_length=63, unique=True)
    servicename = models.CharField(max_length=127, blank=True)
    servicesummary = models.CharField(max_length=255, blank=True)
    targetdetail = models.TextField(blank=True)
    supportstandard = models.TextField(blank=True)
    supportmoney = models.TextField(blank=True)
    servicedetail = models.TextField(blank=True)
    servicedetailimage = models.CharField(max_length=511, blank=True)
    contactinfoname = models.CharField(max_length=127, blank=True)
    contactinfonumber = models.CharField(max_length=31, blank=True)
    sitename = models.CharField(max_length=63, blank=True)
    sitelink = models.CharField(max_length=255, blank=True)
    formname = models.CharField(max_length=63, blank=True)
    formlink = models.CharField(max_length=255, blank=True)
    lawname = models.CharField(max_length=63, blank=True)
    lawlink = models.CharField(max_length=255, blank=True)
    registerdate = models.CharField(max_length=100, blank=True)
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

    class Meta:
        db_table = 'Welfare'


class Weltrgterindvdl(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    trgterindvdlid = models.ForeignKey(
        Trgterindvdlarray,
        on_delete=models.CASCADE,
        db_column='trgterindvdlid'
    )

    class Meta:
        db_table = 'Weltrgterindvdl'


class Weldesire(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    desireid = models.ForeignKey(
        Desirearray,
        on_delete=models.CASCADE,
        db_column='desireid'
    )

    class Meta:
        db_table = 'Weldesire'


class Weldisable(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    disableid = models.ForeignKey(
        Disable,
        on_delete=models.CASCADE,
        db_column='disableid'
    )

    class Meta:
        db_table = 'Weldisable'


class Welchartrgter(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    chartrgterid = models.ForeignKey(
        Chartrgterarray,
        on_delete=models.CASCADE,
        db_column='chartrgterid'
    )

    class Meta:
        db_table = 'Welchartrgter'


class Wellife(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    lifeid = models.ForeignKey(
        Lifearray,
        on_delete=models.CASCADE,
        db_column='lifeid'
    )

    class Meta:
        db_table = 'Wellife'


class Welresponsible(models.Model):
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    responsibleid = models.ForeignKey(
        Responsible,
        on_delete=models.CASCADE,
        db_column='responsibleid'
    )

    class Meta:
        db_table = 'Welresponsible'
