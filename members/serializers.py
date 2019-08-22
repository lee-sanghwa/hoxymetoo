"""
프로그램 ID:SV-1010-PY
프로그램명:serializers.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 회원 model과 view를 이어주는 중간단계의 serializer파일로, view에서 create와 update시에 manytomany에 대한 필드들에 대한 처리를 해주고있다.
"""

from rest_framework import serializers
from django.db import connection
from members.models import Member, Job, MemJob, MemDisable, MemWelfare, MemHouseType, MemDesire, MemTargetCharacter, \
    MemLifeCycle, MemFamily, Family
from welfares.models import HouseType, Desire, TargetCharacter, LifeCycle, Disable, Welfare
from hoxymetoo.key import aes_key


class MemberSerializer(serializers.ModelSerializer):
    # 이 serializer로 create가 호출 되었을 때, 즉 view에서 HTTP Method인 POST가 request 되었을 때
    def create(self, validated_data):
        cursor = connection.cursor()
        unvalidated_data = self.context['request'].data
        jobs = unvalidated_data.get('jobs', [])
        disables = unvalidated_data.get('disables', [])
        welfares = unvalidated_data.get('welfares', [])
        house_types = unvalidated_data.get('houseTypes', [])
        desires = unvalidated_data.get('desires', [])
        target_characters = unvalidated_data.get('targetCharacters', [])
        life_cycles = unvalidated_data.get('lifeCycles', [])
        families = unvalidated_data.get('families', [])

        social_id = validated_data.get('socialId')
        push_token = validated_data.get('pushToken')
        mem_key = validated_data.get('memKey')
        mem_email = validated_data.get('memEmail')
        mem_password = validated_data.get('memPassword')
        mem_receivable_money = validated_data.get('memReceivableMoney')
        mem_birthday = validated_data.get('memBirthday')
        mem_gender = validated_data.get('memGender')
        mem_family = validated_data.get('memFamily')
        mem_income = validated_data.get('memIncome')
        mem_bohun = validated_data.get('memBohun')
        si_do_id = validated_data.get('siDoId')
        si_gun_gu_id = validated_data.get('siGunGuId')
        create_date_time = validated_data.get('createDateTime')
        create_date = validated_data.get('createDate')
        create_time = validated_data.get('createTime')
        update_date_time = validated_data.get('updateDateTime')
        update_date = validated_data.get('updateDate')
        update_time = validated_data.get('updateTime')

        if mem_email is not None:
            aes_encrypt_query_email = "HEX(AES_ENCRYPT('{memEmail}', '{aesKey}'))".format(memEmail=mem_email,
                                                                                          aesKey=aes_key)
            mem_email = aes_encrypt_query_email
        if mem_birthday is not None:
            aes_encrypt_query_birthday = "HEX(AES_ENCRYPT('{memBirthday}', '{aesKey}'))".format(
                memBirthday=mem_birthday, aesKey=aes_key)
            mem_birthday = aes_encrypt_query_birthday
        if mem_gender is not None:
            aes_encrypt_query_gender = "HEX(AES_ENCRYPT('{memGender}', '{aesKey}'))".format(memGender=mem_gender,
                                                                                            aesKey=aes_key)
            mem_gender = aes_encrypt_query_gender
        if mem_family is not None:
            aes_encrypt_query_family = "HEX(AES_ENCRYPT('{memFamily}', '{aesKey}'))".format(memFamily=mem_family,
                                                                                            aesKey=aes_key)
            mem_family = aes_encrypt_query_family
        if mem_income is not None:
            aes_encrypt_query_income = "HEX(AES_ENCRYPT('{memIncome}', '{aesKey}'))".format(memIncome=mem_income,
                                                                                            aesKey=aes_key)
            mem_income = aes_encrypt_query_income
        if mem_bohun is not None:
            aes_encrypt_query_bohun = "HEX(AES_ENCRYPT('{memBohun}', '{aesKey}'))".format(memBohun=mem_bohun,
                                                                                          aesKey=aes_key)
            mem_bohun = aes_encrypt_query_bohun

        if push_token is None:
            push_token = 'NULL'
        if mem_email is None:
            mem_email = 'NULL'
        if mem_password is None:
            mem_password = 'NULL'
        if mem_receivable_money is None:
            mem_receivable_money = 0
        if mem_birthday is None:
            mem_birthday = 'NULL'
        if mem_gender is None:
            mem_gender = 'NULL'
        if mem_family is None:
            mem_family = 'NULL'
        if mem_income is None:
            mem_income = 'NULL'
        if mem_bohun is None:
            mem_bohun = 'NULL'
        if si_do_id is None:
            si_do_id = 'NULL'
        if si_gun_gu_id is None:
            si_gun_gu_id = 'NULL'

        create_query_with_aes_encrypt_string = '''INSERT INTO Member(socialid, pushtoken, memkey, email, password,
                                                                receivablemoney, st_birthday, st_gender, st_family,
                                                                st_income, st_bohun, sidoid, sigunguid, createdatetime,
                                                                createdate, createtime, updatedatetime, updatedate, updatetime)
                                        VALUES ('{socialId}', '{pushToken}', '{memKey}', {memEmail}, {memPassword},
                                                {memReceivableMoney}, {memBirthday}, {memGender}, {memFamily},
                                                {memIncome}, {memBohun}, {siDoId}, {siGunGuId}, '{createDateTime}',
                                                '{createDate}', '{createTime}', '{updateDateTime}', '{updateDate}', '{updateTime}')'''

        cursor.execute(create_query_with_aes_encrypt_string.format(
            socialId=social_id, pushToken=push_token, memKey=mem_key, memEmail=mem_email, memPassword=mem_password,
            memReceivableMoney=mem_receivable_money, memBirthday=mem_birthday, memGender=mem_gender,
            memFamily=mem_family, memIncome=mem_income, memBohun=mem_bohun, siDoId=si_do_id, siGunGuId=si_gun_gu_id,
            createDateTime=create_date_time, createDate=create_date, createTime=create_time,
            updateDateTime=update_date_time, updateDate=update_date, updateTime=update_time
        ))

        instance = Member.objects.get(socialId=social_id)

        # 회원의 직업에 대한 처리
        for job in jobs:
            job_instance = Job.objects.get(jobId=job)
            mem_job_data = {
                'socialId': instance,
                'jobId': job_instance
            }
            MemJob.objects.create(**mem_job_data)

        # 회원의 질병에 대한 처리
        for disable in disables:
            disable_instance = Disable.objects.get(disableId=disable)
            mem_disable_data = {
                'socialId': instance,
                'disableId': disable_instance
            }
            MemDisable.objects.create(**mem_disable_data)

        # 회원이 받을 수 있는 복에 대한 처리 (아마 회원 생성 단계에서는 불가능할 것으로 보임)
        for welfare in welfares:
            welfare_instance = Welfare.objects.get(welId=welfare)
            mem_welfare_data = {
                'socialId': instance,
                'welId': welfare_instance
            }
            MemWelfare.objects.create(**mem_welfare_data)

        # 회원의 가구유형에 대한 처리
        for house_type in house_types:
            house_type_instance = HouseType.objects.get(houseTypeId=house_type)
            mem_house_type_data = {
                'socialId': instance,
                'houseTypeId': house_type_instance
            }
            MemHouseType.objects.create(**mem_house_type_data)

        # 회원의 욕구에 대한 처리
        for desire in desires:
            desire_instance = Desire.objects.get(desireId=desire)
            mem_desire_data = {
                'socialId': instance,
                'desireId': desire_instance
            }
            MemDesire.objects.create(**mem_desire_data)

        # 회원의 대상특성에 대한 처리
        for target_character in target_characters:
            target_character_instance = TargetCharacter.objects.get(targetCharacterId=target_character)
            mem_target_character_data = {
                'socialId': instance,
                'targetCharacterId': target_character_instance
            }
            MemTargetCharacter.objects.create(**mem_target_character_data)

        # 회원의 생애주기에 대한 처리
        for life_cycle in life_cycles:
            life_cycle_instance = LifeCycle.objects.get(lifeCycleId=life_cycle)
            mem_life_cycle_data = {
                'socialId': instance,
                'lifeCycleId': life_cycle_instance
            }
            MemLifeCycle.objects.create(**mem_life_cycle_data)

        # 회원의 가족 구성원에 대한 처리
        for family_member in families:
            family_member_birth = family_member['familyBirth']
            family_member_gender = family_member['familyGender']
            family_member_info = str(family_member_birth) + '-' + str(family_member_gender)
            family_data = {
                'familyBirth': family_member_birth,
                'familyGender': family_member_gender,
                'familyInfo': family_member_info
            }
            family_instance = Family.objects.create(**family_data)

            family_instance_id = family_instance.familyId
            new_family_info = str(family_instance_id) + ':' + family_instance.familyInfo
            family_instance.familyInfo = new_family_info
            family_instance.save()

            mem_family_data = {
                'socialId': instance,
                'familyId': family_instance
            }
            MemFamily.objects.create(**mem_family_data)

        return instance

    # 이 serializer로 update가 호출 되었을 때, 즉 view에서 HTTP Method인 PATCH가 request 되었을 때
    def update(self, instance, validated_data):
        unvalidated_data = self.context['request'].data

        # 입력받은 json들에 대해서는 생성되어야할 것들로 네이밍
        # 기존에 존재하는 데이터데 대해서는 삭제되어야할 것들로 네이밍
        new_jobs = unvalidated_data.get('jobs', [])
        existing_jobs = instance.jobs.all()
        new_disables = unvalidated_data.get('disables', [])
        existing_disables = instance.disables.all()
        new_welfares = unvalidated_data.get('welfares', [])
        existing_welfares = instance.welfares.all()
        new_house_types = unvalidated_data.get('houseTypes', [])
        existing_house_types = instance.houseTypes.all()
        new_desires = unvalidated_data.get('desires', [])
        existing_desires = instance.desires.all()
        new_target_characters = unvalidated_data.get('targetCharacters', [])
        existing_target_characters = instance.targetCharacters.all()
        new_life_cycles = unvalidated_data.get('lifeCycles', [])
        existing_life_cycles = instance.lifeCycles.all()
        new_families = unvalidated_data.get('families', [])
        existing_families = instance.families.all()

        # 임시적인 배열들을 만들어 원래의 데이터들을 건들지 않기를 위함
        will_create_mem_jobs = list(new_jobs)
        will_remove_mem_jobs = list(existing_jobs)
        will_create_mem_disables = list(new_disables)
        will_remove_mem_disables = list(existing_disables)
        will_create_mem_welfares = list(new_welfares)
        will_remove_mem_welfares = list(existing_welfares)
        will_create_mem_house_types = list(new_house_types)
        will_remove_mem_house_types = list(existing_house_types)
        will_create_mem_desires = list(new_desires)
        will_remove_mem_desires = list(existing_desires)
        will_create_mem_target_characters = list(new_target_characters)
        will_remove_mem_target_characters = list(existing_target_characters)
        will_create_mem_life_cycles = list(new_life_cycles)
        will_remove_mem_life_cycles = list(existing_life_cycles)
        will_remove_mem_family = list(existing_families)

        # 입력받은 직업 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_job in new_jobs:
            for existing_job in existing_jobs:
                if existing_job.jobId == new_job:
                    will_create_mem_jobs.remove(existing_job.jobId)

        # 기존에 존재하는 직업 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_job in existing_jobs:
            for new_job in new_jobs:
                if existing_job.jobId == new_job:
                    will_remove_mem_jobs.remove(existing_job)

        # 삭제되어야할 직업 아이디들을 반복
        for will_remove_mem_job in will_remove_mem_jobs:
            # 멤버의 소셜 아이디와 삭제되어야할 직업 아이디로 검색 후 삭제
            MemJob.objects.filter(socialId=instance.socialId, jobId=will_remove_mem_job.jobId).delete()

        # 새롭게 생성되어야할 직업에 대한 처리
        for will_create_mem_job in will_create_mem_jobs:
            job_instance = Job.objects.get(jobId=will_create_mem_job)
            mem_job_data = {
                'socialId': instance,
                'jobId': job_instance
            }
            MemJob.objects.create(**mem_job_data)

        # 입력받은 질병 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_disable in new_disables:
            for existing_disable in existing_disables:
                if existing_disable.disableId == new_disable:
                    will_create_mem_disables.remove(existing_disable.disableId)

        # 기존에 존재하는 질병 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_disable in existing_disables:
            for new_disable in new_disables:
                if existing_disable.disableId == new_disable:
                    will_remove_mem_disables.remove(existing_disable)

        # 삭제되어야할 질병 아이디들을 반복
        for will_remove_mem_disable in will_remove_mem_disables:
            # 멤버의 소셜 아이디와 삭제되어야할 질병 아이디로 검색 후 삭제
            MemDisable.objects.filter(socialId=instance.socialId, disableId=will_remove_mem_disable.disableId).delete()

        # 새롭게 생성되어야할 질병에 대한 처리
        for will_create_mem_disable in will_create_mem_disables:
            disable_instance = Disable.objects.get(disableId=will_create_mem_disable)
            mem_disable_data = {
                'socialId': instance,
                'disableId': disable_instance
            }
            MemDisable.objects.create(**mem_disable_data)

        # 입력받은 복지 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_welfare in new_welfares:
            for existing_welfare in existing_welfares:
                if existing_welfare.welId == new_welfare:
                    will_create_mem_welfares.remove(existing_welfare.welId)

        # 기존에 존재하는 복지 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_welfare in existing_welfares:
            for new_welfare in new_welfares:
                if existing_welfare.welId == new_welfare:
                    will_remove_mem_welfares.remove(existing_welfare)

        # 삭제되어야할 복지 아이디들을 반복
        for will_remove_mem_welfare in will_remove_mem_welfares:
            # 멤버의 소셜 아이디와 삭제되어야할 복지 아이디로 검색 후 삭제
            MemWelfare.objects.filter(socialId=instance.socialId, welId=will_remove_mem_welfare.welId).delete()

        # 새롭게 생성되어야할 복지에 대한 처리
        for will_create_mem_welfare in will_create_mem_welfares:
            welfare_instance = Welfare.objects.get(welId=will_create_mem_welfare)
            mem_welfare_data = {
                'socialId': instance,
                'welId': welfare_instance
            }
            MemWelfare.objects.create(**mem_welfare_data)

        # 입력받은 가구 유형 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_house_type in new_house_types:
            for existing_house_type in existing_house_types:
                if existing_house_type.houseTypeId == new_house_type:
                    will_create_mem_house_types.remove(existing_house_type.houseTypeId)

        # 기존에 존재하는 가구 유형 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_house_type in existing_house_types:
            for new_house_type in new_house_types:
                if existing_house_type.houseTypeId == new_house_type:
                    will_remove_mem_house_types.remove(existing_house_type)

        # 삭제되어야할 가구 유형 아이디들을 반복
        for will_remove_mem_house_type in will_remove_mem_house_types:
            # 멤버의 소셜 아이디와 삭제되어야할 가구 유형 아이디로 검색 후 삭제
            MemHouseType.objects.filter(socialId=instance.socialId,
                                        houseTypeId=will_remove_mem_house_type.houseTypeId).delete()

        # 새롭게 생성되어야할 가구 유형에 대한 처리
        for will_create_mem_house_type in will_create_mem_house_types:
            house_type_instance = HouseType.objects.get(houseTypeId=will_create_mem_house_type)
            mem_house_type_data = {
                'socialId': instance,
                'houseTypeId': house_type_instance
            }
            MemHouseType.objects.create(**mem_house_type_data)

        # 입력받은 욕구 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_desire in new_desires:
            for existing_desire in existing_desires:
                if existing_desire.desireId == new_desire:
                    will_create_mem_desires.remove(existing_desire.desireId)

        # 기존에 존재하는 욕구 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_desire in existing_desires:
            for new_desire in new_desires:
                if existing_desire.desireId == new_desire:
                    will_remove_mem_desires.remove(existing_desire)

        # 삭제되어야할 욕구 아이디들을 반복
        for will_remove_mem_desire in will_remove_mem_desires:
            # 멤버의 소셜 아이디와 삭제되어야할 욕구 아이디로 검색 후 삭제
            MemDesire.objects.filter(socialId=instance.socialId, desireId=will_remove_mem_desire.desireId).delete()

        # 새롭게 생성되어야할 욕구에 대한 처리
        for will_create_mem_desire in will_create_mem_desires:
            desire_instance = Desire.objects.get(desireId=will_create_mem_desire)
            mem_desire_data = {
                'socialId': instance,
                'desireId': desire_instance
            }
            MemDesire.objects.create(**mem_desire_data)

        # 입력받은 대상특성 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_target_character in new_target_characters:
            for existing_target_character in existing_target_characters:
                if existing_target_character.targetCharacterId == new_target_character:
                    will_create_mem_target_characters.remove(existing_target_character.targetCharacterId)

        # 기존에 존재하는 대상특성 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_target_character in existing_target_characters:
            for new_target_character in new_target_characters:
                if existing_target_character.targetCharacterId == new_target_character:
                    will_remove_mem_target_characters.remove(existing_target_character)

        # 삭제되어야할 대상특성 아이디들을 반복
        for will_remove_mem_target_character in will_remove_mem_target_characters:
            # 멤버의 소셜 아이디와 삭제되어야할 대상특성 아이디로 검색 후 삭제
            MemTargetCharacter.objects.filter(socialId=instance.socialId,
                                              targetCharacterId=will_remove_mem_target_character.targetCharacterId).delete()

        # 새롭게 생성되어야할 대상특성에 대한 처리
        for will_create_mem_target_character in will_create_mem_target_characters:
            target_character_instance = TargetCharacter.objects.get(targetCharacterId=will_create_mem_target_character)
            mem_target_character_data = {
                'socialId': instance,
                'targetCharacterId': target_character_instance
            }
            MemTargetCharacter.objects.create(**mem_target_character_data)

        # 입력받은 생애주기 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_life_cycle in new_life_cycles:
            for existing_life_cycle in existing_life_cycles:
                if existing_life_cycle.lifeCycleId == new_life_cycle:
                    will_create_mem_life_cycles.remove(existing_life_cycle.lifeCycleId)

        # 기존에 존재하는 생애주기 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_life_cycle in existing_life_cycles:
            for new_life_cycle in new_life_cycles:
                if existing_life_cycle.lifeCycleId == new_life_cycle:
                    will_remove_mem_life_cycles.remove(existing_life_cycle)

        # 삭제되어야할 생애주기 아이디들을 반복
        for will_remove_mem_life_cycle in will_remove_mem_life_cycles:
            # 멤버의 소셜 아이디와 삭제되어야할 생애주기 아이디로 검색 후 삭제
            MemLifeCycle.objects.filter(socialId=instance.socialId,
                                        lifeCycleId=will_remove_mem_life_cycle.lifeCycleId).delete()

        # 새롭게 생성되어야할 생애주기에 대한 처리
        for will_create_mem_life_cycle in will_create_mem_life_cycles:
            life_cycle_instance = LifeCycle.objects.get(lifeCycleId=will_create_mem_life_cycle)
            mem_life_cycle_data = {
                'socialId': instance,
                'lifeCycleId': life_cycle_instance
            }
            MemLifeCycle.objects.create(**mem_life_cycle_data)

        # 입력받은 가족 구성원 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_family_member in new_families:
            family_id = new_family_member.get('familyId', None)
            new_family_member_birth = new_family_member.get('familyBirth', None)
            new_family_member_gender = new_family_member.get('familyGender', None)
            new_family_member_info = str(new_family_member_birth) + '-' + str(new_family_member_gender)
            # 새로운 가족을 추가하는 경우
            if family_id is None:
                new_family_data = {
                    'familyBirth': new_family_member_birth,
                    'familyGender': new_family_member_gender,
                    'familyInfo': new_family_member_info
                }
                new_family_instance = Family.objects.create(**new_family_data)

                new_family_instance_id = new_family_instance.familyId
                new_family_info = str(new_family_instance_id) + ':' + new_family_instance.familyInfo
                new_family_instance.familyInfo = new_family_info
                new_family_instance.save()

                new_mem_family_data = {
                    'socialId': instance,
                    'familyId': new_family_instance
                }
                MemFamily.objects.create(**new_mem_family_data)
            else:
                existing_family_member = Family.objects.get(familyId=family_id)
                existing_family_member.familyBirth = new_family_member_birth
                existing_family_member.familyGender = new_family_member_gender
                existing_family_member.familyInfo = str(family_id) + ':' + new_family_member_info
                existing_family_member.save()
                # 기존에 존재하는 가족 구성원 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
                will_remove_mem_family.remove(existing_family_member)

        # 삭제되어야할 가족 구성원 아이디들을 반복
        for will_remove_mem_family_member in will_remove_mem_family:
            # 멤버의 소셜 아이디와 삭제되어야할 가족 구성원 아이디로 검색 후 삭제
            Family.objects.get(familyId=will_remove_mem_family_member.familyId).delete()

        return serializers.ModelSerializer.update(self, instance=instance, validated_data=validated_data)

    # 직업에 대한 아이디값을 반환하는 것이 아닌 직업의 이름을 반환하기 위함
    jobs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='jobName'
    )

    # 질병에 대한 아이디값을 반환하는 것이 아닌 질병의 이름를 반환하기 위함
    disables = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='disableName'
    )

    # 가구 유형에 대한 아이디값을 반환하는 것이 아닌 가구 유형의 이름을 반환하기 위함
    houseTypes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='houseTypeName'
    )

    # 욕구에 대한 아이디값을 반환하는 것이 아닌 욕구의 이름을 반환하기 위함
    desires = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='desireName'
    )

    # 대상특성에 대한 아이디값을 반환하는 것이 아닌 대상특성의 이름을 반환하기 위함
    targetCharacters = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='targetCharacterName'
    )

    # 생애주기에 대한 아이디값을 반환하는 것이 아닌 생애주기의 이름을 반환하기 위함
    lifeCycles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='lifeCycleName'
    )

    # 가족 구성원에 대한 아이디값을 반환하는 것이 아닌 가족 구성원의 정보를 반환하기 위함
    families = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='familyInfo'
    )

    class Meta:
        model = Member
        fields = '__all__'
