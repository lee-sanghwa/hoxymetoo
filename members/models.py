from django.db import models


class Job(models.Model):
    jobid = models.IntegerField()
    name = models.CharField(max_length=127)

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
    st_gender = models.SmallIntegerField()
    st_family = models.SmallIntegerField()
    st_income = models.SmallIntegerField()
    st_bohun = models.SmallIntegerField()
    st_address = models.CharField(max_length=127)
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)
    udatetime = models.CharField(max_length=14)
    udate = models.CharField(max_length=8)
    utime = models.CharField(max_length=6)
    jobs = models.ManyToManyField(
        Job,
        db_table= 'Memjob'
    )
    # 채팅 필드 필요
    # 장애 유형 필드 필요

    def __str__(self):
        return '{}'.format(self.socialid)

    class Meta:
        db_table = 'Member'
