from rest_framework import serializers
from rest_framework.views import APIView


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()