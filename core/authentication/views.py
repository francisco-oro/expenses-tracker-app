from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import status
from .serializers import *
from .utils import token_generator
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
                    user.is_active = False

                    user.save()

                    # Path to view
                    # - Getting the domain we are on
                    # - relative url verification
                    # - encode uid
                    # - token
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

                    # Construct the domain
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={'uidb64':uidb64, 'token':token_generator.make_token(user)})

                    activate_url = 'http://'+domain+link

                    email_subject = "Email Verification Required for Your Account | Rumi Press"
                    email_body = f"""Thank you for signing up with our service! We're excited to have you on board. Before you can start using your account, we need to verify your email address. 
 
                        To complete the verification process, please click on the following link: 
                        
                        {activate_url}
                        
                        By verifying your email, you will gain full access to all the features and benefits our platform offers. It will also help us ensure the security and integrity of your account. 
                        
                        If you did not sign up for an account with us, please disregard this email. Your account will not be activated unless you verify your email address. 
                        
                        If you have any questions or need assistance, please don't hesitate to reach out to our support team at [Support Email]. 
                        
                        Thank you for choosing our service! 
                        
                        Best regards, 
                        Francisco Oro  
                        The Rumi Press Website"""
                    

                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'noreply@semycolon.com',
                        [email],
                    )

                    email.send(fail_silently=False)
                    messages.success(request, "Account succesfully created")
                    messages.info(request, "A verification link has been sent to the email address you provided, please activate your account")

                    return redirect('login')

            messages.error(request, 'The username / email is already taken')
            return render(request, 'authentication/register.html')

        messages.error(request, "Invalid data")
        return render(request, "authentication/register.html")
    

class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user=user, token=token):
                messages.success('User has been already activated')
                return redirect('login')

            if user.is_active:
                messages.success('User has been already activated')
                return redirect('login')

            user.is_active = True
            user.save()

            messages.success(request, "Account activated successfully")
            return redirect('login')
        except Exception as e:
            pass

        return render(request, 'authentication/login.html')
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}, you are now logged in")
        
                    return redirect('expenses')
                
                messages.error(request, "Account is not active, please check your email")
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, please try again')
            return render(request, 'authentication/login.html')
        
        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
    

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out")
        return redirect('login')
    

class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')
    
    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "Please supply a valid email")
            return render(request, 'authentication/reset-password.html')
        
        current_site= get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user, 
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }
        
            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'],
                'token':email_contents['token'],
            })

            email_subject = "Password Reset Instructions | Rumi Press"
            
            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                f"""Subject: Password Reset Instructions for Your Rumi Press Account 
                                    
                                    Dear {user[0].username}, 
                                    
                                    We have received a request to reset the password for your Rumi Press account. We understand that forgetting passwords can happen to the best of us, so don't worry – we're here to help you regain access to your account. 
                                    
                                    To reset your password, please follow the steps below: 
                                    
                                    1. Visit your unique reset password link at {reset_url}. 
                                    2. Enter your new password
                                    3. Keep it safe 

                                    Please note that the password reset link is valid for 1 day. If you don't reset your password within this timeframe, you will need to initiate the process again. 
                                    
                                    If you did not request this password reset, please ignore this email. Rest assured that your account is still secure, and no changes have been made. 
                                    
                                    For any further assistance or queries, please feel free to reach out to our support team at [Support Email Address]. We'll be more than happy to assist you. 
                                    
                                    Thank you for choosing Rumi Press! 
                                    
                                    Best regards, 
                                    
                                    Francisco Oro
                                    Rumi Press Support Team""",
                'noreply@semicolon.com',
                [email]
            )
            
            email.send(fail_silently=False)

            messages.success(request, 'We have sent you an email to reset your password')

            return render(request, 'authentication/reset-password.html')

class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str((urlsafe_base64_decode(uidb64)))
            user = User.objects.get(pk = user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, "Pasword reset link is invalid or expired. Please requesta a new one")
                return redirect('reset-password')
            

        except Exception as indetifier:
            messages.info(request, "Pasword reset link is invalid or expired. Please requesta a new one")
            return redirect('reset-password')
        
        return render(request, 'authentication/set-new-password.html', context)
    




    def post(self, request, uidb64, token): 
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return render(request, 'authentication/set-new-password.html', context)

        if len(password1) < 6:
            messages.error(request, "Password is too short")
            return render(request, 'authentication/set-new-password.html', context)
        try:
            user_id = force_str((urlsafe_base64_decode(uidb64)))
            
            user = User.objects.get(pk = user_id)
            user.set_password(password1)
            user.save()

            messages.success(request, "Password reset succesfull. you can log in with your new password")
            return redirect('login')
        
        except Exception as identifier:
            messages.info(request, "Something went wrong")
        return render(request, 'authentication/set-new-password.html', context)





