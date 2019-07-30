from rest_framework import serializers
from welfares.models import Welfare


class WelfareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Welfare
        fields = '__all__'


