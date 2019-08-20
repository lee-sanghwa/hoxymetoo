"""
프로그램 ID:SV-1210-PY
프로그램명:serializers.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 챗팅로그 model과 view를 이어주는 중간단계의 serializer파일로, view에서 어떤 모델과 필드를 사용할 것인지에 대해 정의되어있다.
"""

from rest_framework import serializers
from chatbot.models import ChatLog


class ChatLogSenderSerializer(serializers.ModelSerializer):
    class Meta:
        # ChatLog의 모델로부터 serializer를 생성
        model = ChatLog
        # 이 모델의 모든 필드를 이용한다.
        fields = '__all__'
        extra_kwargs = {'receiverMemKey': {'write_only': True}}


class ChatLogReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        # ChatLog의 모델로부터 serializer를 생성
        model = ChatLog
        # 이 모델의 모든 필드를 이용한다.
        fields = '__all__'
        extra_kwargs = {'senderMemKey': {'write_only': True}}
