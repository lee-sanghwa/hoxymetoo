"""
프로그램 ID:SV-1220-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 채팅과 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
- HTTP METHOD 의 POST에 대해 채팅 시간을 따로 클라이언트에게 받는 것이 아니라 서버에서 처리해준다.
"""

from chatbot.serializers import ChatLogSenderSerializer, ChatLogReceiverSerializer
from chatbot.models import ChatLog
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from datetime import datetime


class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatLog.objects.filter(chatLogId=None)
    serializer_class = ChatLogSenderSerializer

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        chat_log_data = request.data
        now_date_time = datetime.now()

        # 필드 중 생성 날짜. 시간들에 대한 정보를 클라이언트가 아닌 서버에서 생성
        create_date_time = "%04d%02d%02d%02d%02d%02d" % (
            now_date_time.year,
            now_date_time.month,
            now_date_time.day,
            now_date_time.hour,
            now_date_time.minute,
            now_date_time.second
        )
        create_date = create_date_time[:8]
        create_time = create_date_time[8:]

        chat_log_data['createDateTime'] = create_date_time
        chat_log_data['createDate'] = create_date
        chat_log_data['createTime'] = create_time

        # 생성 날짜, 시간에 대한 정보를 바꾸었으니 다시 원상 복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 채팅 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        chat_data = request.GET

        receiver_member_key = chat_data.get('receiverMemKey', None)
        sender_member_key = chat_data.get('senderMemKey', None)

        if receiver_member_key is None and sender_member_key is not None:
            new_queryset = ChatLog.objects.filter(senderMemKey__memKey=sender_member_key)
            new_serializer_class = ChatLogSenderSerializer
            self.queryset = new_queryset
            self.serializer_class = new_serializer_class
        elif receiver_member_key is not None and sender_member_key is None:
            new_queryset = ChatLog.objects.filter(receiverMemKey__memKey=receiver_member_key)
            new_serializer_class = ChatLogReceiverSerializer
            self.queryset = new_queryset
            self.serializer_class = new_serializer_class

        return ListModelMixin.list(self, request, *args, **kwargs);
