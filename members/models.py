from django.db import models
from welfares.models import Disable, Welfare, Lifearray, Chartrgterarray, Desirearray, Trgterindvdlarray


class Job(models.Model):
    jobid = models.IntegerField(unique=True)
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return 'jobid: {} - name: {}'.format(self.jobid, self.name)

    class Meta:
        db_table = 'Job'


class Family(models.Model):
    familybirth = models.CharField(max_length=8)
    familygender = models.IntegerField()
    familyinfo = models.CharField(max_length=10)

    class Meta:
        db_table = 'Family'


class Member(models.Model):
    memid = models.IntegerField(unique=True)
    socialid = models.CharField(max_length=255, unique=True)
    pushtoken = models.CharField(max_length=255, blank=True)
    memkey = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=127, blank=True)
    st_birthday = models.CharField(max_length=8)
    st_gender = models.IntegerField()
    st_family = models.IntegerField()
    st_income = models.IntegerField()
    st_bohun = models.IntegerField(default=0)
    st_address = models.CharField(max_length=127)
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)
    udatetime = models.CharField(max_length=14)
    udate = models.CharField(max_length=8)
    utime = models.CharField(max_length=6)
    jobs = models.ManyToManyField(
        Job,
        through='Memjob'
    )
    disables = models.ManyToManyField(
        Disable,
        through='Memdisable'
    )
    welfares = models.ManyToManyField(
        Welfare,
        through='Memwelfare'
    )
    housetypes = models.ManyToManyField(
        Trgterindvdlarray,
        through='Memtrgterindvdl'
    )
    desires = models.ManyToManyField(
        Desirearray,
        through='Memdesire'
    )
    targetcharacters = models.ManyToManyField(
        Chartrgterarray,
        through='Memchartrgter'
    )
    lifetimes = models.ManyToManyField(
        Lifearray,
        through='Memlife'
    )
    families = models.ManyToManyField(
        Family,
        through='Memfamily'
    )

    def __str__(self):
        return '{}'.format(self.socialid)

    class Meta:
        db_table = 'Member'


class Memjob(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    jobid = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        db_column='jobid'
    )

    class Meta:
        db_table = 'Memjob'


class Memdisable(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    disableid = models.ForeignKey(
        Disable,
        on_delete=models.CASCADE,
        db_column='disableid'
    )

    class Meta:
        db_table = 'Memdisable'


class Memwelfare(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    welid = models.ForeignKey(
        Welfare,
        on_delete=models.CASCADE,
        db_column='welid'
    )
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Memwelfare'


class Memtrgterindvdl(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    trgterindvdlid = models.ForeignKey(
        Trgterindvdlarray,
        on_delete=models.CASCADE,
        db_column='trgterindvdlid'
    )

    class Meta:
        db_table = 'Memtrgterindvdl'


class Memdesire(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    desireid = models.ForeignKey(
        Desirearray,
        on_delete=models.CASCADE,
        db_column='desireid'
    )

    class Meta:
        db_table = 'Memdesire'


class Memchartrgter(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    chartrgterid = models.ForeignKey(
        Chartrgterarray,
        on_delete=models.CASCADE,
        db_column='chartrgterid'
    )

    class Meta:
        db_table = 'Memchartrgter'


class Memlife(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    lifeid = models.ForeignKey(
        Lifearray,
        on_delete=models.CASCADE,
        db_column='lifeid'
    )

    class Meta:
        db_table = 'Memlife'


class Memfamily(models.Model):
    memid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        db_column='memid'
    )
    familyid = models.ForeignKey(
        Family,
        on_delete=models.CASCADE,
        db_column='familyid'
    )

    class Meta:
        db_table = 'Memfamily'


class Chatlog(models.Model):
    senderid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='senderid',
        db_column='senderid'
    )
    receiveid = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='receiveid',
        db_column='receiveid'
    )
    content = models.TextField()
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Chatlog'
