"""
프로그램 ID:SV-1300-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 질문, 답변 관련 내용을 다루고 있다.
"""

from django.db import models


# 데이터베이스의 카테고리 테이블과 연동하기 위한 클래스
class Category(models.Model):
    # 카테고리 아이디 ( 1 ~ )
    categoryId = models.AutoField(
        primary_key=True,
        db_column='categoryid'
    )
    # 카테고리 이름 ( 단순 문의 ~ )
    categoryName = models.CharField(
        max_length=63,
        unique=True,
        db_column='categoryname'
    )

    class Meta:
        # 카테고리 테이블의 이름을 Category 설정 (원래는 qnas_Category)
        db_table = 'Category'


# 데이터베이스의 질문 테이블과 연동하기 위한 클래스
class Question(models.Model):
    # 질문 아이디 ( 1 ~ )
    questionId = models.AutoField(
        primary_key=True,
        db_column='questionid'
    )
    # 카테고리 아이디 ( 1 ~ )
    categoryId = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column='categoryid'
    )
    # 크롤링한 질문 내용 (실업급여 받을 때 어떤 서류가 필요한가요?)
    questionContent = models.TextField(
        null=True,
        db_column='questioncontent'
    )
    # 질문 생성 날짜시간 (20190705230521)
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    # 질문 생성 날짜 (20190705)
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    # 질문 생성 시간 (230521)
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )

    class Meta:
        # 질문 테이블의 이름을 Question 설정 (원래는 qnas_Question)
        db_table = 'Question'


# 데이터베이스의 답변 테이블과 연동하기 위한 클래스
class Answer(models.Model):
    # 답변 아이디 ( 1 ~ )
    answerId = models.AutoField(
        primary_key=True,
        db_column='answerid'
    )
    # 카테고리 아이디 ( 1 ~ )
    categoryId = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        db_column='categoryid'
    )
    # 크롤링한 답변 내용 (실업급여 받을때에는 이러이러한 것들이 필요합니다.)
    answerContent = models.TextField(
        null=True,
        db_column='answercontent'
    )
    # 답변 생성 날짜시간 (20190705230521)
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    # 답변 생성 날짜 (20190705)
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    # 답변 생성 시간 (230521)
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )

    class Meta:
        # 답변 테이블의 이름을 Answer 설정 (원래는 qnas_Answer)
        db_table = 'Answer'


# 데이터베이스의 답변 테이블과 연동하기 위한 클래스
class Qna(models.Model):
    # QNA 아이디 ( 1 ~ )
    qnaId = models.AutoField(
        primary_key=True,
        db_column='qnaid'
    )
    # 질문 아이디 ( 1 ~ )
    questionId = models.OneToOneField(
        Question,
        on_delete=models.CASCADE,
        db_column='questionid'
    )
    # 질문 아이디에 대한 답변의 아이디( 1 ~ )
    answerId = models.OneToOneField(
        Answer,
        on_delete=models.CASCADE,
        db_column='answerid'
    )
    # QnA 생성 날짜시간 (20190705230521)
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    # QnA 생성 날짜 (20190705)
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    # QnA 생성 시간 (230521)
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )

    class Meta:
        # 답변 테이블의 이름을 Qna 설정 (원래는 qnas_Qna)
        db_table = 'Qna'
