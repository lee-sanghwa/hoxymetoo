"""
프로그램 ID:SV-1020-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 회원과 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
- HTTP METHOD에 따라서 CREATE, PATCH에 대해 through를 통해 생성된 manytomany 필드에 대한 유효성 검사
- 서버에서 생성가능한 데이터는 서버에서 처리
"""

from members.models import Member, Job
from welfares.models import HouseType, Desire, TargetCharacter, LifeCycle, Disable, Welfare
from members.serializers import MemberSerializer
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from datetime import datetime
import hashlib


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # memKey로 멤버의 정보 조회 및 업데이트 및 삭제
    lookup_field = 'memKey'

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        member_data = request.data
        social_id = member_data['socialId']
        now_datetime = datetime.now()

        jobs = member_data.get('jobs', [])
        disables = member_data.get('disables', [])
        welfares = member_data.get('welfares', [])
        house_types = member_data.get('houseTypes', [])
        desires = member_data.get('desires', [])
        target_characters = member_data.get('targetCharacters', [])
        life_cycles = member_data.get('lifeCycles', [])

        # 유효성 검사를 거치지않는 필드들에 대해서 따로 검사
        try:
            for job in jobs:
                Job.objects.get(jobId=job)
            for disable in disables:
                Disable.objects.get(disableId=disable)
            for welfare in welfares:
                Welfare.objects.get(welId=welfare)
            for house_type in house_types:
                HouseType.objects.get(houseTypeId=house_type)
            for desire in desires:
                Desire.objects.get(desireId=desire)
            for target_character in target_characters:
                TargetCharacter.objects.get(targetCharacterId=target_character)
            for life_cycle in life_cycles:
                LifeCycle.objects.get(lifeCycleId=life_cycle)
        except Job.DoesNotExist or Disable.DoesNotExist or Welfare.DoesNotExist or HouseType.DoesNotExist or \
               Desire.DoesNotExist or TargetCharacter.DoesNotExist or LifeCycle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        mem_key = hashlib.sha256(social_id.encode()).hexdigest()

        member_data['memKey'] = mem_key
        member_data['createDateTime'] = create_date_time
        member_data['updateDateTime'] = create_date_time
        member_data['createDate'] = create_date
        member_data['updateDate'] = create_date
        member_data['createTime'] = create_time
        member_data['updateTime'] = create_time

        # mutable 원상복구
        request.POST._mutable = mutable

        # 이 데이터를 토대로 멤버 생성
        return CreateModelMixin.create(self, request, *args, **kwargs)

    # HTTP METHOD의 PATCH
    def update(self, request, *args, **kwargs):
        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        member_data = request.data
        now_datetime = datetime.now()

        jobs = member_data.get('jobs')
        disables = member_data.get('disables')
        welfares = member_data.get('welfares')
        house_types = member_data.get('houseTypes')
        desires = member_data.get('desires')
        target_characters = member_data.get('targetCharacters')
        life_cycles = member_data.get('lifeCycles')

        # 유효성 검사를 거치지않는 필드들에 대해서 따로 검사
        try:
            for job in jobs:
                Job.objects.get(jobId=job)
            for disable in disables:
                Disable.objects.get(disableId=disable)
            for welfare in welfares:
                Welfare.objects.get(welId=welfare)
            for house_type in house_types:
                HouseType.objects.get(houseTypeId=house_type)
            for desire in desires:
                Desire.objects.get(desireId=desire)
            for target_character in target_characters:
                TargetCharacter.objects.get(targetCharacterId=target_character)
            for life_cycle in life_cycles:
                LifeCycle.objects.get(lifeCycleId=life_cycle)
        except Job.DoesNotExist or Disable.DoesNotExist or Welfare.DoesNotExist or HouseType.DoesNotExist or \
               Desire.DoesNotExist or TargetCharacter.DoesNotExist or LifeCycle.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 필드 중 생성 날짜. 시간들에 대한 정보를 클라이언트가 아닌 서버에서 생성
        update_date_time = "%04d%02d%02d%02d%02d%02d" % (
            now_datetime.year,
            now_datetime.month,
            now_datetime.day,
            now_datetime.hour,
            now_datetime.minute,
            now_datetime.second
        )
        update_date = update_date_time[:8]
        update_time = update_date_time[8:]

        member_data['updateDateTime'] = update_date_time
        member_data['updateDate'] = update_date
        member_data['updateTime'] = update_time

        request.POST._mutable = mutable
        # 부분적인 업데이트를 한다는 것을 serializer에게 알려줌
        kwargs['partial'] = True

        # 이 데이터를 토대로 멤버 수정
        return UpdateModelMixin.update(self, request, *args, **kwargs)
