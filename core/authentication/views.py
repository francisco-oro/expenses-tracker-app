from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import status
from .serializers import *
from validate_email import validate_email

# Create your views here.

class EmailValidationView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            if User.objects.filter(email=email).exists():
                return Response({"email_error":"Sorry, email is already in use"}, status=status.HTTP_409_CONFLICT)

            return Response({"email_valid": True})
        
        return Response({"email_error":"Email is invalid"}, status=status.HTTP_400_BAD_REQUEST)



class UsernameValidationView(APIView):
    def post(self, request):
        serializer = UsernameSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']

            if not username.isalnum():
                return Response({'username_error':'username should only contain alphanumeric characters'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({"username_error":"username is already taken"}, status=status.HTTP_409_CONFLICT)

            return Response({'username_valid': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors)     
     

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')