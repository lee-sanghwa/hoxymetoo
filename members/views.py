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

from addresses.models import Address
from members.models import Member, Job, MemDesire, MemLifeCycle, MemTargetCharacter, MemHouseType, MemWelfare, Feedback
from welfares.models import HouseType, Desire, TargetCharacter, LifeCycle, Disable, Welfare
from members.serializers import MemberSerializer, FeedbackSerializer
from hoxymetoo.key import aes_key
from hoxymetoo.create_log import create_log_content
from django.db import connection
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.response import Response
from datetime import datetime
import hashlib
import logging

logger = logging.getLogger(__name__)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # memKey로 멤버의 정보 조회 및 업데이트 및 삭제
    lookup_field = 'memKey'

    # HTTP METHOD의 POST
    def create(self, request, *args, **kwargs):
        logger.info("TRY CREATE MEMBER" + create_log_content(request))

        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        member_data = request.data
        social_id = member_data['socialId']
        salting_with_social_id = 'hoxymetoo_' + social_id
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
            logger.error("ERROR with field associated with CREATE MEMBER" + create_log_content(request))
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
        mem_key = hashlib.sha256(salting_with_social_id.encode()).hexdigest()

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
        CreateModelMixin.create(self, request, *args, **kwargs)

        instance = Member.objects.get(socialId=social_id)
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data

        list_of_welfare_of_recommend = self.select_welfare_of_member(social_id)
        for welfare_of_recommend in list_of_welfare_of_recommend:
            MemWelfare.objects.get_or_create(socialId=instance, welId=welfare_of_recommend)

        member_data = self.changeAddressToString(serializer_data)
        decrypt_member_data = self.decryptMemberData(social_id=social_id, member_data=member_data)
        return Response(decrypt_member_data)

    # HTTP METHOD의 PATCH
    def update(self, request, *args, **kwargs):
        logger.info("TRY UPDATE MEMBER" + create_log_content(request))

        # Django 에서는 request의 body로 들어온 정보를 변환하지 못하도록 막았기 때문에 이를 풀어줌
        mutable = request.POST._mutable
        request.POST._mutable = True

        member_data = request.data
        social_id = member_data['socialId']
        salting_with_social_id = 'hoxymetoo_' + social_id
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
            logger.error("ERROR with field associated with UPDATE MEMBER" + create_log_content(request))
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
        mem_key = hashlib.sha256(salting_with_social_id.encode()).hexdigest()

        member_data['memKey'] = mem_key
        member_data['updateDateTime'] = update_date_time
        member_data['updateDate'] = update_date
        member_data['updateTime'] = update_time

        request.POST._mutable = mutable
        # 부분적인 업데이트를 한다는 것을 serializer에게 알려줌
        kwargs['partial'] = True

        # 이 데이터를 토대로 멤버 수정
        UpdateModelMixin.update(self, request, *args, **kwargs)

        instance = Member.objects.get(socialId=social_id)
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data

        MemWelfare.objects.filter(socialId=instance).delete()

        list_of_welfare_of_recommend = self.select_welfare_of_member(social_id)
        for welfare_of_recommend in list_of_welfare_of_recommend:
            MemWelfare.objects.get_or_create(socialId=instance, welId=welfare_of_recommend)

        member_data = self.changeAddressToString(serializer_data)
        decrypt_member_data = self.decryptMemberData(social_id=social_id, member_data=member_data)
        return Response(decrypt_member_data)

    def list(self, request, *args, **kwargs):
        logger.info("TRY LIST MEMBER" + create_log_content(request))

        new_queryset = Member.objects.all()
        # 보안성을 위해 배포시에 주석 해제
        # new_queryset = Member.objects.filter(socialId=None)
        social_id = request.GET.get('socialId', None)

        if social_id is not None:
            try:
                instance = Member.objects.get(socialId=social_id)
            except Member.DoesNotExist:
                message = {
                    'message': '해당하는 socialId가 존재하지 않습니다.'
                }
                return Response(message, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(instance)
            serializer_data = serializer.data
            member_data = self.changeAddressToString(serializer_data)
            decrypt_member_data = self.decryptMemberData(social_id=social_id, member_data=member_data)
            return Response(decrypt_member_data)

        self.queryset = new_queryset

        return ListModelMixin.list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info("TRY RETRIEVE MEMBER" + create_log_content(request))

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data

        member_data = self.changeAddressToString(serializer_data)
        decrypt_member_data = self.decryptMemberData(social_id=instance.socialId, member_data=member_data)

        return Response(decrypt_member_data)

    def changeAddressToString(self, serializer_data):
        mem_address_id = serializer_data['memAddressId']

        if mem_address_id is not None:
            mem_address_name = Address.objects.get(addressId=mem_address_id).siDoSiGunGuName
            serializer_data['memAddressId'] = mem_address_name

        return serializer_data

    def decryptMemberData(self, social_id, member_data):
        cursor = connection.cursor()
        column_names = {'memEmail': 'email', 'memBirthday': 'st_birthday', 'memGender': 'st_gender',
                        'memFamily': 'st_family', 'memIncome': 'st_income', 'memBohun': 'st_bohun'}
        decrypt_mem_column_query_string = '''
            SELECT CAST( AES_DECRYPT(UNHEX({column}), '{aesKey}') AS CHAR) AS {column}
            FROM Member
            WHERE socialid='{socialId}'
        '''

        for column_name_item in column_names.items():
            cursor.execute(
                decrypt_mem_column_query_string.format(column=column_name_item[1], aesKey=aes_key, socialId=social_id))
            tuple_query_return = cursor.fetchone()
            decrypt_column_data = tuple_query_return[0]
            member_data[column_name_item[0]] = decrypt_column_data

        return member_data

    def select_welfare_of_member(self, social_id):
        address_id_of_member = Member.objects.get(socialId=social_id).memAddressId_id
        if address_id_of_member is None:
            address_id_of_member = 27

        all_kind_of_character = ("desire", "lifeCycle", "targetCharacter", "houseType")
        query_of_create_welfare_of_member = """
        SELECT TEMP.welid, TEMP.weladdressid, COUNT(TEMP.welid) AS cnt
        FROM (
        """

        flag_of_writing_union = False
        has_character = len(all_kind_of_character)

        for kind_of_character in all_kind_of_character:
            list_of_character_id = self.select_member_character(social_id, kind_of_character)
            query = self.make_query_for_welfare_of_member(kind_of_character, list_of_character_id)

            if query == "":
                has_character -= 1
            else:
                if flag_of_writing_union:
                    query_of_create_welfare_of_member += """
                    UNION ALL
                    """

                query_of_create_welfare_of_member += query
                flag_of_writing_union = True

        query_of_create_welfare_of_member += f"""
        ) TEMP
        WHERE TEMP.weladdressid = 27
        OR TEMP.weladdressid = {address_id_of_member} 
        GROUP BY TEMP.welid
        ORDER BY cnt DESC
        LIMIT 1000
        """

        if has_character == 0:
            list_of_recommend_welfare = Welfare.objects.filter(
                Q(welAddressId=address_id_of_member) | Q(welAddressId=27))
        else:
            list_of_recommend_welfare = Welfare.objects.raw(query_of_create_welfare_of_member)

        return list_of_recommend_welfare

    # 멤버의 특정 특이점에 대한 테이블에 대해 특이점 id들을 반환
    def select_member_character(self, social_id, kind_of_character):
        all_kind_of_character = {
            "desire": MemDesire,
            "lifeCycle": MemLifeCycle,
            "targetCharacter": MemTargetCharacter,
            "houseType": MemHouseType
        }

        json_of_constraint = {"socialId": social_id}
        table_of_character = all_kind_of_character.get(kind_of_character)
        column_of_character = kind_of_character + "Id"

        list_of_character_id = []
        if table_of_character is not None:
            rows_of_character = table_of_character.objects.filter(**json_of_constraint)

            for row_of_character in rows_of_character:
                list_of_character_id.append(
                    getattr(getattr(row_of_character, column_of_character), column_of_character))

        return list_of_character_id

    # houseType, ['001',]
    # => 쿼리 생성
    def make_query_for_welfare_of_member(self, name_of_character, list_of_character_id):
        # housetype
        lower_of_name_of_character = name_of_character.lower()

        # Welhousetype
        table_name = "Wel" + lower_of_name_of_character
        # housetypeid
        column_name = lower_of_name_of_character + "id"

        query = ""

        if len(list_of_character_id) > 0:
            query += f"""
            SELECT Welfare.welid, Welfare.weladdressid
	        FROM Welfare
            JOIN {table_name} ON {table_name}.welid = Welfare.welid
            WHERE {table_name}.{column_name} = '{list_of_character_id[0]}'
            """

            for character_id in list_of_character_id[1:]:
                query += f"""
                OR {table_name}.{column_name} = '{character_id}'
                """

        return query


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
