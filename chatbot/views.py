from chatbot.serializers import ChatlogSerializer
from chatbot.models import Chatlog
from rest_framework import viewsets
from datetime import datetime


class ChatbotViewSet(viewsets.ModelViewSet):
    queryset = Chatlog.objects.all()
    serializer_class = ChatlogSerializer

    def create(self, request, *args, **kwargs):
        member_data = request.data
        now_datetime = datetime.now()

        cdatetime = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        cdate = cdatetime[:8]
        ctime = cdatetime[8:]

        member_data['cdatetime'] = cdatetime
        member_data['cdate'] = cdate
        member_data['ctime'] = ctime

        super().create(request, *args, **kwargs)