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
from welfares.models import WelIndex
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from datetime import datetime


class ChatBotViewSet(viewsets.ModelViewSet):
    queryset = ChatLog.objects.all()
    # 보안성을 위해 배포시에 주석 해제
    # queryset = ChatLog.objects.filter(chatLogId=None)
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
        search = chat_data.get('search', None)

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

        if search is not None:
            from gensim.models import Word2Vec
            from konlpy.tag import Okt
            import sys

            okt = Okt()

            token_list = okt.pos(phrase=search, stem=True, norm=True)  # 단어 토큰화

            model = Word2Vec.load(f'{sys.path[0]}/chatbot/word2vec.model')

            dict_similar_tokens = dict()
            for token in token_list:
                if token[1] in ['Noun']:
                    try:
                        similar_tokens = model.wv.most_similar(token[0])
                    except KeyError:
                        continue
                    if similar_tokens:
                        dict_similar_tokens[token[0]] = similar_tokens

            recommend_welfare = dict()
            for key, similar_keys in dict_similar_tokens.items():
                list_recommend_welfare_index = WelIndex.objects.filter(indexName=key)
                for recommend_welfare_index in list_recommend_welfare_index:
                    welfare_count = recommend_welfare.get(recommend_welfare_index.welId)
                    if welfare_count is None:
                        recommend_welfare[recommend_welfare_index.welId] = 1
                    else:
                        recommend_welfare[recommend_welfare_index.welId] = welfare_count + 1

                for similar_key in similar_keys:
                    list_recommend_welfare_index = WelIndex.objects.filter(indexName=similar_key)
                    for recommend_welfare_index in list_recommend_welfare_index:
                        welfare_count = recommend_welfare.get(recommend_welfare_index.welId)
                        if welfare_count is None:
                            recommend_welfare[recommend_welfare_index.welId] = 1
                        else:
                            recommend_welfare[recommend_welfare_index.welId] = welfare_count + 1

            recommend_welfares_sorted_by_count_desc = sorted(recommend_welfare, key=recommend_welfare.get, reverse=True)
            recommend_welfare_dict = dict()
            for recommend_welfare_sorted_by_count_desc in recommend_welfares_sorted_by_count_desc:
                recommend_welfare_dict[recommend_welfare_sorted_by_count_desc] = recommend_welfare.get(
                    recommend_welfare_sorted_by_count_desc)

            return Response(recommend_welfare_dict)

        return ListModelMixin.list(self, request, *args, **kwargs)
