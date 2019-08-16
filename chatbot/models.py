"""
프로그램 ID:SV-1200-PY
프로그램명:models.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- ERD를 통해 데이터베이스 스크립트를 생성하여 실제 데이터베이스에 만들어진 테이블들과 연동하기위한 것으로, 채팅관련 내용을 다루고 있다.
"""

from django.db import models
from members.models import Member


# 데이터베이스의 채팅관련 테이블과 연동하기 위한 클래스
class ChatLog(models.Model):
    # 채팅 기록의 아이디 ( 1 ~ )
    chatLogId = models.AutoField(
        primary_key=True,
        db_column='chatlogid'
    )
    # 채팅을 보내는 회원의 소셜 로그인의 아이디 ( kakao_32A3DB124 )
    senderId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='senderid',
        db_column='senderid'
    )
    # 채팅을 받는 회원의 소셜 로그인의 아이디 ( kakao_32A3DB124 )
    receiverId = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='receiverid',
        db_column='receiverid'
    )
    # 메세지 내용 (실업급여에 필요한 서류 알려줘)
    chatLogContent = models.TextField(
        db_column='chatlogcontent'
    )
    # 채팅 생성 날짜시간(예: 20190702180514)
    createDateTime = models.CharField(
        max_length=14,
        db_column='createdatetime'
    )
    # 채팅 생성 날짜 (예: 20190702)
    createDate = models.CharField(
        max_length=8,
        db_column='createdate'
    )
    # 채팅 생성 시간(예: 180514)
    createTime = models.CharField(
        max_length=6,
        db_column='createtime'
    )

    class Meta:
        # 채팅관련 테이블의 이름을 Chatlog 설정 (원래는 chatbot_ChatLog)
        db_table = 'Chatlog'
