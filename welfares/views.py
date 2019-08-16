"""
프로그램 ID:SV-1120-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 복지와 관련한 view 파일로, 클라이언트와 서버간의 통신이 이루어지는 부분이다.
- HTTP METHOD에 따라서 CREATE, PATCH에 대해 through를 통해 생성된 manytomany 필드에 대한 유효성 검사
"""

from welfares.models import Welfare, Disable, HouseType, Desire, TargetCharacter, LifeCycle, Responsible
from welfares.serializers import WelfareSerializer
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response


class WelfareViewSet(viewsets.ModelViewSet):
    queryset = Welfare.objects.all()
    serializer_class = WelfareSerializer

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        welfare_data = request.data

        disables = welfare_data.get('disables', [])
        welfares = welfare_data.get('welfares', [])
        house_types = welfare_data.get('houseTypes', [])
        desires = welfare_data.get('desires', [])
        target_characters = welfare_data.get('targetCharacters', [])
        life_cycles = welfare_data.get('lifeCycles', [])
        responsibles = welfare_data.get('responsibles', [])

        # 유효성 검사를 거치지않는 필드들에 대해서 따로 검사
        try:
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
            for responsible in responsibles:
                Responsible.objects.get(responsibleId=responsible)
        except Disable.DoesNotExist or Welfare.DoesNotExist or HouseType.DoesNotExist or TargetCharacter.DoesNotExist \
               or LifeCycle.DoesNotExist or Responsible.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return CreateModelMixin.create(self, request, *args, **kwargs)

    # HTTP METHOD의 PATCH
    def update(self, request, *args, **kwargs):
        welfare_data = request.data

        disables = welfare_data.get('disables')
        welfares = welfare_data.get('welfares')
        house_types = welfare_data.get('houseTypes')
        desires = welfare_data.get('desires')
        target_characters = welfare_data.get('targetCharacters')
        life_cycles = welfare_data.get('lifeCycles')
        responsibles = welfare_data.get('responsibles')

        # 유효성 검사를 거치지않는 필드들에 대해서 따로 검사
        try:
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
            for responsible in responsibles:
                Responsible.objects.get(responsibleId=responsible)
        except Disable.DoesNotExist or Welfare.DoesNotExist or HouseType.DoesNotExist or TargetCharacter.DoesNotExist \
               or LifeCycle.DoesNotExist or Responsible.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # 부분적인 업데이트를 한다는 것을 serializer에게 알려줌
        kwargs['partial'] = True

        return UpdateModelMixin.partial_update(self, request, *args, **kwargs)
