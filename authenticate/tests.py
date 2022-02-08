from django.test import TestCase, Client

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import mail
import re

from .models import UserInfo

User = get_user_model()
c = Client()

class ProfileTest(TestCase):

    def setUp(self):
        basic_user = User(username='user', email='user@google.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('user')
        basic_user.save()
        self.basic_user = basic_user
        self.basic_user_password = 'user'
        self.basic_user_email = 'user@google.com'

    def test_importing_model(self):
        print('[AUTH] Проверка импортирования модели UserInfo []')
        try:
            from .models import UserInfo
            import_status = True
        except:
            import_status = False

        self.assertTrue(import_status, msg='Модель UserInfo не импортирована!')
        print('[AUTH] Проверка импортирования модели UserInfo [x]')

    def test_registration_url(self):
        print('[AUTH] Проверка url регистрации []')
        registration_url = '/auth/register/'
        response = c.get(registration_url)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url регистрации [x]')


    def test_registration_request(self):
        print('[AUTH] Проверка регистрации пользователя []')
        registration_url = '/auth/register/'
        data = {
            'username': self.basic_user,
            'email': self.basic_user_email,
            'password1': self.basic_user_password,
            'password2': self.basic_user_password
        }
        response = c.post(registration_url, data, follow=True)
        response_status = response.status_code
        self.assertEqual(response_status, 200)
        print('[AUTH] Проверка регистрации пользователя [x]')

    def test_login_url(self):
        print('[AUTH] Проверка url у логина []')
        login_url = '/auth/login/'
        self.assertEqual(settings.LOGIN_URL, login_url)
        print('[AUTH] Проверка url у логина [x]')
    
    def test_login_request(self):
        print('[AUTH] Проверка входа пользователя в аккаунт []')
        login_url = settings.LOGIN_URL
        data = {
            'username': self.basic_user,
            'password': self.basic_user_password,
        }
        response = c.post(login_url, data, follow=True)
        response_status = response.status_code
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, settings.LOGIN_REDIRECT_URL)
        self.assertEqual(response_status, 200)
        print('[AUTH] Проверка входа пользователя в аккаунт [x]')
    