from django.db import models
from welfares.models import Disable, Welfare


class Job(models.Model):
    jobid = models.IntegerField(unique=True)
    name = models.CharField(max_length=127, unique=True)

    def __str__(self):
        return 'jobid: {} - name: {}'.format(self.jobid, self.name)

    class Meta:
        db_table = 'Job'


class Member(models.Model):

    memid = models.IntegerField(unique=True)
    socialid = models.CharField(max_length=255, unique=True)
    pushtoken = models.CharField(max_length=255, unique=True)
    memkey = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=127)
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
        through= 'Memjob'
    )
    disables = models.ManyToManyField(
        Disable,
        through= 'Memdisable'
    )
    welfares = models.ManyToManyField(
        Welfare,
        through='Memwelfare'
    )
    # 채팅 필드 필요

    def __str__(self):
        return '{}'.format(self.socialid)

    class Meta:
        db_table = 'Member'


class Memjob(models.Model):
    memid = models.ForeignKey(Member)
    jobid = models.ForeignKey(Job)

    class Meta:
        db_table = 'Memjob'


class Memdisable(models.Model):
    memid = models.ForeignKey(Member)
    disableid = models.ForeignKey(Disable)

    class Meta:
        db_table = 'Memdisable'


class Memwelfare(models.Model):
    memid = models.ForeignKey(Member)
    welid = models.ForeignKey(Welfare)
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Memwelfare'
