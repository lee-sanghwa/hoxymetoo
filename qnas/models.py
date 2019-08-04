from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        db_table = 'Category'


class Question(models.Model):
    qcontent = models.TextField()
    categoryid = models.IntegerField()
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Question'


class Answer(models.Model):
    acontent = models.TextField()
    categoryid = models.IntegerField()
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Answer'


class Qna(models.Model):
    qid = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        db_column='qid'
    )
    aid = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        db_column='aid'
    )
    cdatetime = models.CharField(max_length=14)
    cdate = models.CharField(max_length=8)
    ctime = models.CharField(max_length=6)

    class Meta:
        db_table = 'Qna'
