from rest_framework import serializers
from chatbot.models import Chatlog

class ChatlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatlog
        fields = '__all__'