"""
프로그램 ID:SV-1110-PY
프로그램명:views.py
작성자:이상화(developerjosephlee97@gmail.com)
생성일자:2019-08-16
버전:0.5
설명:
- 복지관련 model과 view를 이어주는 중간단계의 serializer파일로, view에서 어떤 모델과 필드를 사용할 것인지에 대해 정의되어있다.
"""

from rest_framework import serializers
from welfares.models import Welfare, HouseType, WelHouseType, DisableType, DisableLevel, Disable, WelDisable, Desire, \
    WelDesire, TargetCharacter, WelTargetCharacter, LifeCycle, WelLifeCycle, Responsible, WelResponsible, Index, \
    WelIndex


class WelfareSerializer(serializers.ModelSerializer):
    # 이 serializer로 create가 호출 되었을 때, 즉 view에서 HTTP Method인 POST가 request 되었을 때
    def create(self, validated_data):
        unvalidated_data = self.context['request'].data
        house_types = unvalidated_data.get('houseTypes', [])
        disables = unvalidated_data.get('disables', [])
        desires = unvalidated_data.get('desires', [])
        target_characters = unvalidated_data.get('targetCharacters', [])
        life_cycles = unvalidated_data.get('lifeCycles', [])
        responsibles = unvalidated_data.get('responsibles', [])

        # view에서 유효성검사를 거친 데이터들로 멤버 생성
        instance = Welfare.objects.create(**validated_data)

        # 복지와 관련된 가구유형에 대한 처리
        for house_type in house_types:
            house_type_instance = HouseType.objects.get(houseTypeId=house_type)
            wel_house_type_data = {
                'welId': instance,
                'houseTypeId': house_type_instance
            }
            WelHouseType.objects.create(**wel_house_type_data)

        # 복지와 관련된 질병에 대한 처리
        for disable in disables:
            disable_instance = Disable.objects.get(disableId=disable)
            wel_disable_data = {
                'welId': instance,
                'disableId': disable_instance
            }
            WelDisable.objects.create(**wel_disable_data)

        # 복지와 관련된 욕구에 대한 처리
        for desire in desires:
            desire_instance = Desire.objects.get(desireId=desire)
            wel_desire_data = {
                'welId': instance,
                'desireId': desire_instance
            }
            WelDesire.objects.create(**wel_desire_data)

        # 복지에 해당하는 대상특성에 대한 처리
        for target_character in target_characters:
            target_character_instance = TargetCharacter.objects.get(targetCharacterId=target_character)
            wel_target_character_data = {
                'welId': instance,
                'targetCharacterId': target_character_instance
            }
            WelTargetCharacter.objects.create(**wel_target_character_data)

        # 복지와 관련된 생애주기에 대한 처리
        for life_cycle in life_cycles:
            life_cycle_instance = LifeCycle.objects.get(lifeCycleId=life_cycle)
            wel_life_cycle_data = {
                'welId': instance,
                'lifeCycleId': life_cycle_instance
            }
            WelLifeCycle.objects.create(**wel_life_cycle_data)

        # 복지와 관련된 책임기관에 대한 처리
        for responsible in responsibles:
            responsible_instance = Responsible.objects.get(responsibleId=responsible)
            wel_responsible_data = {
                'welId': instance,
                'responsibleId': responsible_instance
            }
            WelResponsible.objects.create(**wel_responsible_data)

        return instance

    # 이 serializer로 update가 호출 되었을 때, 즉 view에서 HTTP Method인 PATCH가 request 되었을 때
    def update(self, instance, validated_data):
        unvalidated_data = self.context['request'].data

        # 입력받은 json들에 대해서는 생성되어야할 것들로 네이밍
        # 기존에 존재하는 데이터데 대해서는 삭제되어야할 것들로 네이밍
        new_disables = unvalidated_data.get('disables', [])
        existing_disables = instance.disables.all()
        new_house_types = unvalidated_data.get('houseTypes', [])
        existing_house_types = instance.houseTypes.all()
        new_desires = unvalidated_data.get('desires', [])
        existing_desires = instance.desires.all()
        new_target_characters = unvalidated_data.get('targetCharacters', [])
        existing_target_characters = instance.targetCharacters.all()
        new_life_cycles = unvalidated_data.get('lifeCycles', [])
        existing_life_cycles = instance.lifeCycles.all()

        # 임시적인 배열들을 만들어 원래의 데이터들을 건들지 않기를 위함
        will_create_wel_disables = list(new_disables)
        will_remove_wel_disables = list(existing_disables)
        will_create_wel_house_types = list(new_house_types)
        will_remove_wel_house_types = list(existing_house_types)
        will_create_wel_desires = list(new_desires)
        will_remove_wel_desires = list(existing_desires)
        will_create_wel_target_characters = list(new_target_characters)
        will_remove_wel_target_characters = list(existing_target_characters)
        will_create_wel_life_cycles = list(new_life_cycles)
        will_remove_wel_life_cycles = list(existing_life_cycles)

        # 입력받은 복지의 질병 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_disable in new_disables:
            for existing_disable in existing_disables:
                if existing_disable.disableId == new_disable:
                    will_create_wel_disables.remove(existing_disable.disableId)

        # 기존에 존재하는 복지의 질병 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_disable in existing_disables:
            for new_disable in new_disables:
                if existing_disable.disableId == new_disable:
                    will_remove_wel_disables.remove(existing_disable)

        # 삭제되어야할 복지의 질병 아이디들을 반복
        for will_remove_wel_disable in will_remove_wel_disables:
            # 복지의 아이디와 삭제되어야할 질병 아이디로 검색 후 삭제
            WelDisable.objects.filter(welId=instance.socialId, disableId=will_remove_wel_disable.disableId).delete()

        # 새롭게 생성되어야할 복지의 질병에 대한 처리
        for will_create_wel_disable in will_create_wel_disables:
            disable_instance = Disable.objects.get(disableId=will_create_wel_disable)
            wel_disable_data = {
                'welId': instance,
                'disableId': disable_instance
            }
            WelDisable.objects.create(**wel_disable_data)

        # 입력받은 복지의 가구 유형 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_house_type in new_house_types:
            for existing_house_type in existing_house_types:
                if existing_house_type.houseTypeId == new_house_type:
                    will_create_wel_house_types.remove(existing_house_type.houseTypeId)

        # 기존에 존재하는 복지의 가구 유형 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_house_type in existing_house_types:
            for new_house_type in new_house_types:
                if existing_house_type.houseTypeId == new_house_type:
                    will_remove_wel_house_types.remove(existing_house_type)

        for will_remove_wel_house_type in will_remove_wel_house_types:
            # 복지의 아이디와 삭제되어야할 가구 유형 아이디로 검색 후 삭제
            WelHouseType.objects.filter(welId=instance.socialId,
                                        houseTypeId=will_remove_wel_house_type.houseTypeId).delete()

        # 새롭게 생성되어야할 복지의 가구 유형에 대한 처리
        for will_create_wel_house_type in will_create_wel_house_types:
            house_type_instance = HouseType.objects.get(houseTypeId=will_create_wel_house_type)
            wel_house_type_data = {
                'welId': instance,
                'houseTypeId': house_type_instance
            }
            WelHouseType.objects.create(**wel_house_type_data)

        # 입력받은 복지의 욕구 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_desire in new_desires:
            for existing_desire in existing_desires:
                if existing_desire.desireId == new_desire:
                    will_create_wel_desires.remove(existing_desire.desireId)

        # 기존에 존재하는 복지의 욕구 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_desire in existing_desires:
            for new_desire in new_desires:
                if existing_desire.desireId == new_desire:
                    will_remove_wel_desires.remove(existing_desire)

        # 삭제되어야할 복지의 욕구 아이디들을 반복
        for will_remove_wel_desire in will_remove_wel_desires:
            # 복지의 아이디와 삭제되어야할 욕구 아이디로 검색 후 삭제
            WelDesire.objects.filter(welId=instance.socialId, desireId=will_remove_wel_desire.desireId).delete()

        # 새롭게 생성되어야할 복지의 욕구에 대한 처리
        for will_create_wel_desire in will_create_wel_desires:
            desire_instance = Desire.objects.get(desireId=will_create_wel_desire)
            wel_desire_data = {
                'welId': instance,
                'desireId': desire_instance
            }
            WelDesire.objects.create(**wel_desire_data)

        # 입력받은 복지의 대상특성 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_target_character in new_target_characters:
            for existing_target_character in existing_target_characters:
                if existing_target_character.targetCharacterId == new_target_character:
                    will_create_wel_target_characters.remove(existing_target_character.targetCharacterId)

        # 기존에 존재하는 복지의 대상특성 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_target_character in existing_target_characters:
            for new_target_character in new_target_characters:
                if existing_target_character.targetCharacterId == new_target_character:
                    will_remove_wel_target_characters.remove(existing_target_character)

        # 삭제되어야할 복지의 대상특성 아이디들을 반복
        for will_remove_wel_target_character in will_remove_wel_target_characters:
            # 복지의 아이디와 삭제되어야할 대상특성 아이디로 검색 후 삭제
            WelTargetCharacter.objects.filter(welId=instance.socialId,
                                              targetCharacterId=will_remove_wel_target_character.targetCharacterId).delete()

        # 새롭게 생성되어야할 복지의 대상특성에 대한 처리
        for will_create_wel_target_character in will_create_wel_target_characters:
            target_character_instance = TargetCharacter.objects.get(targetCharacterId=will_create_wel_target_character)
            wel_target_character_data = {
                'welId': instance,
                'targetCharacterId': target_character_instance
            }
            WelTargetCharacter.objects.create(**wel_target_character_data)

        # 입력받은 복지의 생애주기 배열에서, 기존에 존재하는 값과 비교하여 추가된 값을 배열에 담는 과정 (입력받은 배열에서 삭제를 통하여)
        for new_life_cycle in new_life_cycles:
            for existing_life_cycle in existing_life_cycles:
                if existing_life_cycle.lifeCycleId == new_life_cycle:
                    will_create_wel_life_cycles.remove(existing_life_cycle.lifeCycleId)

        # 기존에 존재하는 복지의 생애주기 배열에서, 입력으로 받은 값과 비교하여 삭제된 값을 배열에 담는 과정 (기존에 존재하는 배열에서 삭제를 통하여)
        for existing_life_cycle in existing_life_cycles:
            for new_life_cycle in new_life_cycles:
                if existing_life_cycle.lifeCycleId == new_life_cycle:
                    will_remove_wel_life_cycles.remove(existing_life_cycle)

        # 삭제되어야할 복지의 생애주기 아이디들을 반복
        for will_remove_wel_life_cycle in will_remove_wel_life_cycles:
            # 복지의 아이디와 삭제되어야할 생애주기 아이디로 검색 후 삭제
            WelLifeCycle.objects.filter(welId=instance.socialId,
                                        lifeCycleId=will_remove_wel_life_cycle.lifeCycleId).delete()

        # 새롭게 생성되어야할 복지의 생애주기에 대한 처리
        for will_create_wel_life_cycle in will_create_wel_life_cycles:
            life_cycle_instance = LifeCycle.objects.get(lifeCycleId=will_create_wel_life_cycle)
            wel_life_cycle_data = {
                'welId': instance,
                'lifeCycleId': life_cycle_instance
            }
            WelLifeCycle.objects.create(**wel_life_cycle_data)

        return serializers.ModelSerializer.update(self, instance=instance, validated_data=validated_data)

    # 가구 유형에 대한 아이디값을 반환하는 것이 아닌 가구 유형의 이름을 반환하기 위함
    houseTypes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='houseTypeName'
    )
    # 질병에 대한 아이디값을 반환하는 것이 아닌 질병의 이름를 반환하기 위함
    disables = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='disableName'
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

    class Meta:
        model = Welfare
        fields = '__all__'


class IndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Index
        fields = '__all__'


class WelfareIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = WelIndex
        fields = '__all__'


class DisableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisableType
        fields = '__all__'


class DisableLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisableLevel
        fields = '__all__'


class DisableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disable
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseType
        fields = '__all__'


class DesireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desire
        fields = '__all__'


class TargetCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetCharacter
        fields = '__all__'


class LifeCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeCycle
        fields = '__all__'
