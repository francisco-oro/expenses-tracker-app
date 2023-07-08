from rest_framework import serializers
from rest_framework.views import APIView


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()