from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Base user and User 2 have the same username
# Base user and User 3 have the same email address

class RegistrationTest(TestCase):
    def setUp(self) -> None:
        self.register_url = reverse("register")
        self.user = {
            'email': 'testemail@rumipress.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.user_2 = {
            'email': 'testemail2@rumipress.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.user_3 = {
            'email': 'testemail@rumipress.com',
            'username': 'testuser2',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.user_short_password = {
            'email': 'testemail@rumipress.com',
            'username': 'testuser',
            'password1': 'test',
            'password2': 'test',
        }
        self.user_unmatching_passwords = {
            'email': 'testemail@rumipress.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword1',
        }
        self.user_invalid_email = {
            'email': 'testemail.com',
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword1',
        }
        return super().setUp()
    
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url,self.user,format="text/html")
        self.assertEqual(response.status_code, 302)
    

    def test_can_register_user_shortpassword(self):
        response = self.client.post(self.register_url,self.user_short_password,format="text/html")
        self.assertEqual(response.status_code, 400)

    def test_can_register_user_unmatchingpasswords(self):
        response = self.client.post(self.register_url,self.user_unmatching_passwords,format="text/html")
        self.assertEqual(response.status_code, 400)

    def test_can_register_user_with_invalid_email(self):
        response = self.client.post(self.register_url,self.user_invalid_email,format="text/html")
        self.assertEqual(response.status_code, 400)

    def test_can_register_user_with_taken_email(self):
        self.client.post(self.register_url,self.user,format="text/html")
        response = self.client.post(self.register_url,self.user_2,format="text/html")
        self.assertEqual(response.status_code, 409)

    def test_can_register_user_with_taken_username(self):
        self.client.post(self.register_url,self.user,format="text/html")
        response = self.client.post(self.register_url,self.user_3,format="text/html")
        self.assertEqual(response.status_code, 409)


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.login_url = reverse('login')
        self.register_url = reverse("register")
        self.user = {
            'email': 'testemail@rumipress.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        return super().setUp()
    
    def test_can_access(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_succes(self):
        self.client.post(self.register_url,self.user,format="text/html")
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True 
        user.save()
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 302)

    def test_login_unverified_email(self):
        self.client.post(self.register_url,self.user,format="text/html")
        response = self.client.post(self.login_url, self.user, format='text/html')
        self.assertEqual(response.status_code, 401)

    def login_with_no_username(self):
        response = self.client.post(self.login_url, {'username':'','password':'password'}, format='text/html')
        self.assertEqual(response.status_code, 401)

    def login_with_no_password(self):
        response = self.client.post(self.login_url, {'username':'testuser', 'password':''}, format='text/html')
        self.assertEqual(response.status_code, 401)
