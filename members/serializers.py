from rest_framework import serializers
from members.models import Member, Job, Memjob, Memdisable, Memwelfare, Memtrgterindvdl, Memdesire, Memchartrgter, \
    Memlife, Memfamily, Family
from welfares.models import Trgterindvdlarray, Desirearray, Chartrgterarray, Lifearray, Disable, Welfare


class MemberSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        unvalidated_data = self.context['request'].data
        jobs = unvalidated_data.get('jobs', [])
        disables = unvalidated_data.get('disables', [])
        welfares = unvalidated_data.get('welfares', [])
        house_types = unvalidated_data.get('housetypes', [])
        desires = unvalidated_data.get('desires', [])
        target_characters = unvalidated_data.get('targetcharacters', [])
        lifetimes = unvalidated_data.get('lifetimes', [])
        family = unvalidated_data.get('family', [])

        instance = Member.objects.create(**validated_data)

        for job in jobs:
            job_instance = Job.objects.get(id=job)
            mem_job_data = {
                'memid': instance,
                'jobid': job_instance
            }
            Memjob.objects.create(**mem_job_data)

        for disable in disables:
            disable_instance = Disable.objects.get(id=disable)
            mem_disable_data = {
                'memid': instance,
                'disableid': disable_instance
            }
            Memdisable.objects.create(**mem_disable_data)

        for welfare in welfares:
            welfare_instance = Welfare.objects.get(id=welfare)
            mem_welfare_data = {
                'memid': instance,
                'welid': welfare_instance
            }
            Memwelfare.objects.create(**mem_welfare_data)

        for house_type in house_types:
            house_type_instance = Trgterindvdlarray.objects.get(id=house_type)
            mem_house_type_data = {
                'memid': instance,
                'trgterindvdlid': house_type_instance
            }
            Memjob.objects.create(**mem_house_type_data)

        for desire in desires:
            desire_instance = Desirearray.objects.get(id=desire)
            mem_desire_data = {
                'memid': instance,
                'desireid': desire_instance
            }
            Memjob.objects.create(**mem_desire_data)

        for target_character in target_characters:
            target_character_instance = Chartrgterarray.objects.get(id=target_character)
            mem_target_character_data = {
                'memid': instance,
                'chartrgterid': target_character_instance
            }
            Memjob.objects.create(**mem_target_character_data)

        for lifetime in lifetimes:
            lifetime_instance = Lifearray.objects.get(id=lifetime)
            mem_lifetime_data = {
                'memid': instance,
                'jobid': lifetime_instance
            }
            Memjob.objects.create(**mem_lifetime_data)

        for family_member in family:
            family_member_birth = family_member['familybirth']
            family_member_gender = family_member['familygender']
            family_member_info = str(family_member_birth) + '-' + str(family_member_gender)
            family_data = {
                'familybirth': family_member_birth,
                'familygender': family_member_gender,
                'familyinfo': family_member_info
            }
            family_instance = Family.objects.create(**family_data)
            mem_family_data = {
                'memid': instance,
                'familyid': family_instance
            }
            Memfamily.objects.create(**mem_family_data)

        return instance

    def update(self, instance, validated_data):
        unvalidated_data = self.context['request'].data

        new_jobs = unvalidated_data.get('jobs', [])
        existing_jobs = instance.jobs.all()
        new_disables = unvalidated_data.get('disables', [])
        existing_disables = instance.disables.all()
        new_welfares = unvalidated_data.get('welfares', [])
        existing_welfares = instance.welfares.all()
        new_house_types = unvalidated_data.get('housetypes', [])
        existing_house_types = instance.housetypes.all()
        new_desires = unvalidated_data.get('desires', [])
        existing_desires = instance.desires.all()
        new_target_characters = unvalidated_data.get('targetcharacters', [])
        existing_target_characters = instance.targetcharacters.all()
        new_lifetimes = unvalidated_data.get('lifetimes', [])
        existing_lifetimes = instance.lifetimes.all()
        new_family = unvalidated_data.get('family', [])
        existing_family = instance.families.all()

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
        will_create_mem_lifetimes = list(new_lifetimes)
        will_remove_mem_lifetimes = list(existing_lifetimes)
        will_remove_mem_family = list(existing_family)

        ##############################################################################################
        for new_job in new_jobs:
            for existing_job in existing_jobs:
                if existing_job.id == new_job:
                    will_create_mem_jobs.remove(existing_job.id)

        for existing_job in existing_jobs:
            for new_job in new_jobs:
                if existing_job.id == new_job:
                    will_remove_mem_jobs.remove(existing_job)

        for will_remove_mem_job in will_remove_mem_jobs:
            Memjob.objects.filter(memid=instance.id, jobid=will_remove_mem_job.id).delete()

        for will_create_mem_job in will_create_mem_jobs:
            job_instance = Job.objects.get(id=will_create_mem_job)
            mem_job_data = {
                'memid': instance,
                'jobid': job_instance
            }
            Memjob.objects.create(**mem_job_data)
        ##############################################################################################
        for new_disable in new_disables:
            for existing_disable in existing_disables:
                if existing_disable.id == new_disable:
                    will_create_mem_disables.remove(existing_disable.id)

        for existing_disable in existing_disables:
            for new_disable in new_disables:
                if existing_disable.id == new_disable:
                    will_remove_mem_disables.remove(existing_disable)

        for will_remove_disable in will_remove_mem_disables:
            Memdisable.objects.filter(memid=instance.id, disableid=will_remove_disable.id).delete()

        for will_create_disable in will_create_mem_disables:
            disable_instance = Disable.objects.get(id=will_create_disable)
            memdisable_data = {
                'memid': instance,
                'disableid': disable_instance
            }
            Memdisable.objects.create(**memdisable_data)
        ##############################################################################################
        for new_welfare in new_welfares:
            for existing_welfare in existing_welfares:
                if existing_welfare.id == new_welfare:
                    will_create_mem_welfares.remove(existing_welfare.id)

        for existing_welfare in existing_welfares:
            for new_welfare in new_welfares:
                if existing_welfare.id == new_welfare:
                    will_remove_mem_welfares.remove(existing_welfare)

        for will_remove_memwelfare in will_remove_mem_welfares:
            Memwelfare.objects.filter(memid=instance.id, welid=will_remove_memwelfare.id).delete()

        for will_create_memwelfare in will_create_mem_welfares:
            welfare_instance = Welfare.objects.get(id=will_create_memwelfare)
            memwelfare_data = {
                'memid': instance,
                'welid': welfare_instance
            }
            Memwelfare.objects.create(**memwelfare_data)

        ##############################################################################################
        for new_house_type in new_house_types:
            for existing_house_type in existing_house_types:
                if existing_house_type.id == new_house_type:
                    will_create_mem_house_types.remove(existing_house_type.id)

        for existing_house_type in existing_house_types:
            for new_house_type in new_house_types:
                if existing_house_type.id == new_house_type:
                    will_remove_mem_house_types.remove(existing_house_type)

        for will_remove_mem_house_type in will_remove_mem_house_types:
            Memtrgterindvdl.objects.filter(memid=instance.id, trgterindvdlid=will_remove_mem_house_type.id).delete()

        for will_create_mem_house_type in will_create_mem_house_types:
            house_type_instance = Trgterindvdlarray.objects.get(id=will_create_mem_house_type)
            mem_house_type_data = {
                'memid': instance,
                'trgterindvdlid': house_type_instance
            }
            Memtrgterindvdl.objects.create(**mem_house_type_data)

        ##############################################################################################
        for new_desire in new_desires:
            for existing_desire in existing_desires:
                if existing_desire.id == new_desire:
                    will_create_mem_desires.remove(existing_desire.id)

        for existing_desire in existing_desires:
            for new_desire in new_desires:
                if existing_desire.id == new_desire:
                    will_remove_mem_desires.remove(existing_desire)

        for will_remove_mem_desire in will_remove_mem_desires:
            Memdesire.objects.filter(memid=instance.id, desireid=will_remove_mem_desire.id).delete()

        for will_create_mem_desire in will_create_mem_desires:
            desire_instance = Desirearray.objects.get(id=will_create_mem_desire)
            mem_desire_data = {
                'memid': instance,
                'desireid': desire_instance
            }
            Memdesire.objects.create(**mem_desire_data)

        ##############################################################################################
        for new_target_character in new_target_characters:
            for existing_target_character in existing_target_characters:
                if existing_target_character.id == new_target_character:
                    will_create_mem_target_characters.remove(existing_target_character.id)

        for existing_target_character in existing_target_characters:
            for new_target_character in new_target_characters:
                if existing_target_character.id == new_target_character:
                    will_remove_mem_target_characters.remove(existing_target_character)

        for will_remove_mem_target_character in will_remove_mem_target_characters:
            Memchartrgter.objects.filter(memid=instance.id, chartrgterid=will_remove_mem_target_character.id).delete()

        for will_create_mem_target_character in will_create_mem_target_characters:
            chartrgter_instance = Chartrgterarray.objects.get(id=will_create_mem_target_character)
            mem_target_character_data = {
                'memid': instance,
                'chartrgterid': chartrgter_instance
            }
            Memchartrgter.objects.create(**mem_target_character_data)

        ##############################################################################################
        for new_lifetime in new_lifetimes:
            for existing_lifetime in existing_lifetimes:
                if existing_lifetime.id == new_lifetime:
                    will_create_mem_lifetimes.remove(existing_lifetime.id)

        for existing_lifetime in existing_lifetimes:
            for new_lifetime in new_lifetimes:
                if existing_lifetime.id == new_lifetime:
                    will_remove_mem_lifetimes.remove(existing_lifetime)

        for will_remove_mem_lifetime in will_remove_mem_lifetimes:
            Memlife.objects.filter(memid=instance.id, lifeid=will_remove_mem_lifetime.id).delete()

        for will_create_mem_lifetime in will_create_mem_lifetimes:
            lifetime_instance = Lifearray.objects.get(id=will_create_mem_lifetime)
            mem_lifetime_data = {
                'memid': instance,
                'lifeid': lifetime_instance
            }
            Memwelfare.objects.create(**mem_lifetime_data)

        ##############################################################################################
        for new_family_member in new_family:
            family_id = new_family_member.get('id')
            new_family_member_birth = new_family_member['familybirth']
            new_family_member_gender = new_family_member['familygender']
            new_family_member_info = str(new_family_member_birth) + ':' + str(new_family_member_gender)
            if family_id is None:
                new_family_data = {
                    'familybirth': new_family_member_birth,
                    'familygender': new_family_member_gender,
                    'familyinfo': new_family_member_info
                }
                new_family_instance = Family.objects.create(**new_family_data)
                new_mem_family_data = {
                    'memid': instance,
                    'familyid': new_family_instance
                }
                Memfamily.objects.create(**new_mem_family_data)
            else:
                existing_family = Family.objects.get(id=family_id)
                existing_family.familybirth = new_family_member_birth
                existing_family.familygender = new_family_member_gender
                existing_family.familyinfo = new_family_member_info
                existing_family.save()

        for existing_family_member in existing_family:
            for new_family_member in new_family:
                if new_family_member.get('id') is not None:
                    if existing_family_member.id == new_family_member:
                        will_remove_mem_family.remove(existing_family_member)

        for will_remove_mem_family_member in will_remove_mem_family:
            Family.objects.get(id=will_remove_mem_family_member.id).delete()

        return instance

    jobs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Member
        fields = '__all__'
