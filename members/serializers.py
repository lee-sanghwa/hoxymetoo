from rest_framework import serializers
from members.models import Member, Job, Memjob, Memdisable, Memwelfare
from welfares.models import Disable, Welfare


class MemberSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        unvalidated_data = self.context['request'].data
        jobs = unvalidated_data.get('jobs', [])
        disables = unvalidated_data.get('disables', [])
        welfares =  unvalidated_data.get('welfares', [])

        instance = Member.objects.create(**validated_data)

        for job in jobs:
            job_instance = Job.objects.get(id=job)
            memjob_data = {
                'memid': instance,
                'jobid': job_instance
            }
            Memjob.objects.create(**memjob_data)

        for disable in disables:
            disable_instance = Disable.objects.get(id=disable)
            memdisable_data = {
                'memid': instance,
                'disableid': disable_instance
            }
            Memdisable.objects.create(**memdisable_data)

        for welfare in welfares:
            welfare_instance = Welfare.objects.get(id=welfare)
            memwelfare_data = {
                'memid': instance,
                'welid': welfare_instance
            }
            Memwelfare.objects.create(**memwelfare_data)

        return instance

    def update(self, instance, validated_data):
        unvalidated_data = self.context['request'].data

        new_jobs = unvalidated_data.get('jobs', [])
        existing_jobs = instance.jobs.all()
        new_disables = unvalidated_data.get('disables', [])
        existing_disables = instance.disables.all()
        new_welfares = unvalidated_data.get('welfares', [])
        existing_welfares = instance.welfares.all()

        will_create_memjobs = list(new_jobs)
        will_remove_memjobs = list(existing_jobs)
        will_create_memdisables = list(new_disables)
        will_remove_memdisables = list(existing_disables)
        will_create_memwelfares = list(new_welfares)
        will_remove_memwelfares = list(existing_welfares)
##############################################################################################
        for new_job in new_jobs:
            for existing_job in existing_jobs:
                if existing_job.id == new_job:
                    will_create_memjobs.remove(existing_job.id)

        for existing_job in existing_jobs:
            for new_job in new_jobs:
                if existing_job.id == new_job:
                    will_remove_memjobs.remove(existing_job)

        for will_remove_memjob in will_remove_memjobs:
            Memjob.objects.filter(memid=instance.id, jobid=will_remove_memjob.id).delete()

        for will_create_memjob in will_create_memjobs:
            job_instance = Job.objects.get(id=will_create_memjob)
            memjob_data = {
                'memid': instance,
                'jobid': job_instance
            }
            Memjob.objects.create(**memjob_data)
##############################################################################################
        for new_disable in new_disables:
            for existing_disable in existing_disables:
                if existing_disable.id == new_disable:
                    will_create_memdisables.remove(existing_disable.id)

        for existing_disable in existing_disables:
            for new_disable in new_disables:
                if existing_disable.id == new_disable:
                    will_remove_memdisables.remove(existing_disable)

        for will_remove_disable in will_remove_memdisables:
            Memdisable.objects.filter(memid=instance.id, disableid=will_remove_disable.id).delete()

        for will_create_disable in will_create_memdisables:
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
                    will_create_memwelfares.remove(existing_welfare.id)

        for existing_welfare in existing_welfares:
            for new_welfare in new_welfares:
                if existing_welfare.id == new_welfare:
                    will_remove_memwelfares.remove(existing_welfare)

        for will_remove_memwelfare in will_remove_memwelfares:
            Memwelfare.objects.filter(memid=instance.id, welid=will_remove_memwelfare.id).delete()

        for will_create_memwelfare in will_create_memwelfares:
            welfare_instance = Welfare.objects.get(id=will_create_memwelfare)
            memwelfare_data = {
                'memid': instance,
                'welid': welfare_instance
            }
            Memwelfare.objects.create(**memwelfare_data)

        return instance

    jobs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Member
        fields = '__all__'





