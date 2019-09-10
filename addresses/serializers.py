from rest_framework import serializers
from addresses.models import SiDo, SiGunGu, Address


class SiDoSerializer(serializers.ModelSerializer):
    class Meta:
        # ChatLog의 모델로부터 serializer를 생성
        model = SiDo
        # 이 모델의 모든 필드를 이용한다.
        fields = '__all__'


class SiGunGuSerializer(serializers.ModelSerializer):
    class Meta:
        # ChatLog의 모델로부터 serializer를 생성
        model = SiGunGu
        # 이 모델의 모든 필드를 이용한다.
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        # ChatLog의 모델로부터 serializer를 생성
        model = Address
        # 이 모델의 모든 필드를 이용한다.
        fields = '__all__'
