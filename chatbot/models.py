from django.db import models
from members.models import Member


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
