"""
프로그램 ID:SV-1320-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- QnA과 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
- HTTP METHOD 의 POST에 대해 qna등록 시간을 따로 클라이언트에게 받는 것이 아니라 서버에서 처리해준다.
"""

from qnas.serializers import CategorySerializer, QuestionSerializer, AnswerSerializer, QnaSerializer
from qnas.models import Question, Answer, Qna, Category
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from datetime import datetime


# 카테고리 view에서는 따로 서버에서 추가되어야하는 정보가없으므로 기존 라이브러리를 사용한다.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        question_data = request.data
        now_datetime = datetime.now()

        # 필드 중 생성 날짜. 시간들에 대한 정보를 클라이언트가 아닌 서버에서 생성
        create_date_time = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        create_date = create_date_time[:8]
        create_time = create_date_time[8:]

        question_data['createDateTime'] = create_date_time
        question_data['createDate'] = create_date
        question_data['createTime'] = create_time

        # 생성 날짜, 시간에 대한 정보를 바꾸었으니 다시 원상 복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 채팅 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def create(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        answer_data = request.data
        now_datetime = datetime.now()

        # 필드 중 생성 날짜. 시간들에 대한 정보를 클라이언트가 아닌 서버에서 생성
        create_date_time = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        create_date = create_date_time[:8]
        create_time = create_date_time[8:]

        answer_data['createDateTime'] = create_date_time
        answer_data['createDate'] = create_date
        answer_data['createTime'] = create_time

        # 생성 날짜, 시간에 대한 정보를 바꾸었으니 다시 원상 복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 채팅 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)


class QnaViewSet(viewsets.ModelViewSet):
    queryset = Qna.objects.all()
    serializer_class = QnaSerializer

    def create(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        qna_data = request.data
        now_datetime = datetime.now()

        # 필드 중 생성 날짜. 시간들에 대한 정보를 클라이언트가 아닌 서버에서 생성
        create_date_time = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        create_date = create_date_time[:8]
        create_time = create_date_time[8:]

        qna_data['createDateTime'] = create_date_time
        qna_data['createDate'] = create_date
        qna_data['createTime'] = create_time

        # 생성 날짜, 시간에 대한 정보를 바꾸었으니 다시 원상 복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 채팅 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)
