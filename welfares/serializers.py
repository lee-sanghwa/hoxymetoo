from rest_framework import serializers
from welfares.models import Welfare, Trgterindvdlarray, Weltrgterindvdl, Disable, Weldisable, Desirearray, Weldesire, \
    Chartrgterarray, Welchartrgter, Lifearray, Wellife


class WelfareSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        unvalidated_data = self.context['request'].data
        house_types = unvalidated_data.get('housetypes', [])
        disables = unvalidated_data.get('disables', [])
        desires = unvalidated_data.get('desires', [])
        target_characters = unvalidated_data.get('targetcharacters', [])
        lifetimes = unvalidated_data.get('lifetimes', [])

        instance = Welfare.objects.create(**validated_data)

        for house_type in house_types:
            house_type_instance = Trgterindvdlarray.objects.get(id=house_type)
            wel_trgterindvdl_data = {
                'welid': instance,
                'trgterindvdlid': house_type_instance
            }
            Weltrgterindvdl.objects.create(**wel_trgterindvdl_data)

        for disable in disables:
            disable_instance = Disable.objects.get(id=disable)
            wel_disable_data = {
                'welid': instance,
                'disableid': disable_instance
            }
            Weldisable.objects.create(**wel_disable_data)

        for desire in desires:
            desire_instance = Desirearray.objects.get(id=desire)
            wel_desire_data = {
                'welid': instance,
                'desireid': desire_instance
            }
            Weldesire.objects.create(**wel_desire_data)

        for target_character in target_characters:
            target_character_instance = Chartrgterarray.objects.get(id=target_character)
            wel_target_character_data = {
                'welid': instance,
                'chartrgterid': target_character_instance
            }
            Welchartrgter.objects.create(**wel_target_character_data)

        for lifetime in lifetimes:
            lifetime_instance = Lifearray.objects.get(id=lifetime)
            wel_lifetime_data = {
                'welid': instance,
                'lifeid': lifetime_instance
            }
            Wellife.objects.create(**wel_lifetime_data)

        return instance

    housetypes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='trgterindvdlname'
    )
    disables = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='disablename'
    )
    desires = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='desirename'
    )
    targetcharacters = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='chartrgtername'
    )
    lifetimes = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='lifename'
    )

    class Meta:
        model = Welfare
        fields = '__all__'
