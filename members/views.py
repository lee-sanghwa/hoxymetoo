from .models import Member
from .serializers import MemberSerializer
from rest_framework import viewsets
from datetime import datetime
import hashlib


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    lookup_field = 'memkey'

    def create(self, request, *args, **kwargs):
        member_data = request.data
        latest_member_id = Member.objects.latest('id').id
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
        memid = str(100000000 + latest_member_id + 1)
        memkey = hashlib.sha256(memid.encode()).hexdigest()

        member_data['memid'] = memid
        member_data['memkey'] = memkey
        member_data['cdatetime'] = cdatetime
        member_data['udatetime'] = cdatetime
        member_data['cdate'] = cdate
        member_data['udate'] = cdate
        member_data['ctime'] = ctime
        member_data['utime'] = ctime

        super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        member_data = request.data
        now_datetime = datetime.now()
        udatetime = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        udate = udatetime[:8]
        utime = udatetime[8:]

        member_data['udatetime'] = udatetime
        member_data['udate'] = udate
        member_data['utime'] = utime

        super().update(request, *args, **kwargs)
