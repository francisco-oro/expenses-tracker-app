from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import status
from .serializers import *
from validate_email import validate_email
import re

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
     

class PasswordValidationView(APIView):
    def post(self, request):
        serializer = PasswordSerializer(data = request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']

            if len(password) < 8:  
                return Response({"password_error": "password is too short"}, status=status.HTTP_400_BAD_REQUEST)  
            
            if not re.search("[a-z]", password):  
                return Response({"password_error": "Password must include at least 2 lowercase and capital letters"}, status=status.HTTP_400_BAD_REQUEST)  
            
            if not re.search("[A-Z]", password):  
                return Response({"password_error": "Password must include at least 2 lowercase and capital letters"}, status=status.HTTP_400_BAD_REQUEST)  
            
            if not re.search("[0-9]", password):  
                return Response({"password_error": "Password must include at least 1 number"}, status=status.HTTP_400_BAD_REQUEST)    
            
            return Response({'password_valid': True}, status=status.HTTP_200_OK)

        return Response({"password_error":"invalid"}, status=status.HTTP_400_BAD_REQUEST)
    

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # TODO Get User data
        # TODO Validate 
        # TODO Create a user account

        serializer = UserRegistrationSerializer(data=request.POST)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']
        
            
            context = {
                'fieldValues': request.POST
            }

            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    if  password1 != password2:
                        messages.error(request, 'Passwords do not match')
                        return render(request, 'authentication/register.html', context)
                    
                    if len(password1) < 8:
                        messages.error(request, "Password is too short")
                        return render(request, 'authentication/register.html', context)
                    
                    user = User.objects.create(username=username,email=email)
                    user.set_password(password1)
                    user.save()

                    messages.success(request, "Account succesfully created")
                    return redirect('register')

            messages.error(request, 'The username / email is already taken')
            return render(request, 'authentication/register.html')

        messages.error(request, "Invalid data")
        return render(request, "authentication/register.html")