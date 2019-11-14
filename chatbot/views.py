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
from welfares.models import Index, WelIndex
from hoxymetoo.create_log import create_log_content
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatLog.objects.all()
    # 보안성을 위해 배포시에 주석 해제
    # queryset = ChatLog.objects.filter(chatLogId=None)
    serializer_class = ChatLogSenderSerializer

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        logger.info("TRY CREATE CHATBOT  ||" + create_log_content(request))
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
        # 20191123 => 2019년 11월 23
        create_date = create_date_time[:8]
        # 193043일 => 19시 30분 43초
        create_time = create_date_time[8:]

        chat_log_data['createDateTime'] = create_date_time
        chat_log_data['createDate'] = create_date
        chat_log_data['createTime'] = create_time

        # 생성 날짜, 시간에 대한 정보를 바꾸었으니 다시 원상 복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 채팅 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        logger.info("TRY LIST CHATBOT  ||" + create_log_content(request))
        chat_data = request.GET

        receiver_member_key = chat_data.get('receiverMemKey', None)
        sender_member_key = chat_data.get('senderMemKey', None)
        search = chat_data.get('search', None)

        # queryset과 serializer_class를 재지정 시작

        # 챗봇을 보낸 사람을 기준으로 list를 호출할 때,
        if receiver_member_key is None and sender_member_key is not None:
            new_queryset = ChatLog.objects.filter(senderMemKey__memKey=sender_member_key)
            new_serializer_class = ChatLogSenderSerializer
            self.queryset = new_queryset
            self.serializer_class = new_serializer_class
        # 챗봇을 받은 사람을 기준으로 list를 호출할 때,
        elif receiver_member_key is not None and sender_member_key is None:
            new_queryset = ChatLog.objects.filter(receiverMemKey__memKey=receiver_member_key)
            new_serializer_class = ChatLogReceiverSerializer
            self.queryset = new_queryset
            self.serializer_class = new_serializer_class

        # queryset과 serializer_class를 재지정 끝

        # search로 파라미터를 받았을 때는 토큰화를 통해 word2vec을 이용하여 복지 검색
        if search is not None:
            from gensim.models import Word2Vec
            from konlpy.tag import Okt
            import sys

            # tagger class를 Okt를 이
            okt = Okt()

            # 단어 토큰화
            token_list = okt.pos(phrase=search, stem=True, norm=True)

            model = Word2Vec.load(f'{sys.path[0]}/chatbot/word2vec.model')

            dict_similar_tokens = dict()
            # 일치율이 높은 3개의 단어만 추출
            n = 3
            # 총 3개 이상의 인덱스가 겹치는 복지의 경우만 반환
            total_count = 3
            for token in token_list:
                if token[1] in ['Noun']:
                    # 사용자의 질문자체를 이용한 유사한 단어 추출
                    try:
                        similar_tokens = model.wv.most_similar(token[0])
                    # 모델에 있지않은 단어의 경우 그냥 계속 작동
                    except KeyError:
                        continue
                    # 사용자의 질문자체에서 뽑힌 단어중 일치율이 높은 n개의 단어만 추출
                    if similar_tokens:
                        dict_similar_tokens[token[0]] = similar_tokens[:n]

            recommend_welfare = dict()
            # ('육아', ('도우미', 0.7666430473327637))
            for key, similar_keys in dict_similar_tokens.items():
                # 사용자의 질문자체의 Noun에 대한 index정보 획득
                try:
                    recommend_index = Index.objects.get(indexName=key)
                # 사용자의 질문자체가 인덱스로 등록 안되어있는 경우에 대한 예외처
                except Index.DoesNotExist:
                    recommend_index = 1560
                # 사용자의 질문자체의 Noun에 대한 index를 갖는 복지들 획득
                list_recommend_welfare_index = WelIndex.objects.filter(indexId=recommend_index)
                for recommend_welfare_index in list_recommend_welfare_index:
                    welfare_count = recommend_welfare.get(recommend_welfare_index.welId.welId)
                    # 처음 검색된 복지일 때, 카운트 = 1
                    if welfare_count is None:
                        recommend_welfare[recommend_welfare_index.welId.welId] = 1
                    # 이미 찾아진 복지일 떄, 카운트 += 1
                    else:
                        recommend_welfare[recommend_welfare_index.welId.welId] = welfare_count + 1

                # 사용자의 질문과 일치율이 높은 단어들에 대해서
                for similar_key in similar_keys:
                    # 일치율이 높은 단어에 대한 index정보 획득
                    recommend_index = Index.objects.get(indexName=similar_key[0])
                    # 일치율이 높은 단어에 대한 index를 갖는 복지들 획득
                    list_recommend_welfare_index = WelIndex.objects.filter(indexId=recommend_index)
                    for recommend_welfare_index in list_recommend_welfare_index:
                        welfare_count = recommend_welfare.get(recommend_welfare_index.welId.welId)
                        # 처음 검색된 복지일 때, 카운트 = 1
                        if welfare_count is None:
                            recommend_welfare[recommend_welfare_index.welId.welId] = 1
                        # 이미 찾아진 복지일 떄, 카운트 += 1
                        else:
                            recommend_welfare[recommend_welfare_index.welId.welId] = welfare_count + 1

            # 카운트가 높은 순으로 정렬
            recommend_welfares_sorted_by_count_desc = sorted(recommend_welfare, key=recommend_welfare.get, reverse=True)

            # 카운트가 특정 수를 넘어야 추천
            recommend_welfare_dict = dict()
            for recommend_welfare_sorted_by_count_desc in recommend_welfares_sorted_by_count_desc:
                if recommend_welfare.get(recommend_welfare_sorted_by_count_desc) >= total_count:
                    recommend_welfare_dict[recommend_welfare_sorted_by_count_desc] = recommend_welfare.get(
                        recommend_welfare_sorted_by_count_desc)

            # 채팅이 어떻게 쪼개졌나 확인하기
            recommend_welfare_dict['chat tokenize'] = token_list

            # 쪼개진 채팅을 토대로 어떤 단어가 유사하다고 나왔는지 확인
            for chat_token, similar_chat_token in dict_similar_tokens.items():
                recommend_welfare_dict[chat_token] = similar_chat_token

            # 이 데이터를 토대로 search에 대한 결과갑 반환
            return Response(recommend_welfare_dict)

        # 이 데이터를 토대로 채팅 반환
        return ListModelMixin.list(self, request, *args, **kwargs)
