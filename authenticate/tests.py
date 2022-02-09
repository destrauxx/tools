from ast import Bytes
from urllib import request
from django.test import TestCase, Client

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core import mail
from django.urls import reverse
from PIL import Image
from io import BytesIO
import re

from .models import UserInfo
from .forms import UserCustomizationForm

User = get_user_model()
c = Client()

def create_image(filename, size=(70, 70), image_format="png", image_mode="RGB"):
    # создаём поток, использующий буфер байтов в памяти.
    data = BytesIO()
    # создаём картинку с заданным размером и форматом
    Image.new(image_mode, size).save(data, image_format)
    # Перемещает указатель текущей позиции в файле в его начало. Я надеюсь ты понял хоть что-нибудь =/ Я сам в этом не до конца разобрался
    data.seek(0)
    return data

class ProfileTest(TestCase):

    def setUp(self):
        basic_user = User(username='admin', email='a@a.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('123')
        basic_user.save()
        basic_user_info.save()
        self.basic_user = basic_user
        self.basic_user_password = 'a'
        self.basic_user_email = 'a@a.com'

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
    
    def test_user_exists(self):
        print('[AUTH] Проверка существования пользователя в базе []')
        user_exists = User.objects.filter(pk=1).exists()
        if user_exists:
            b_user = User.objects.get(pk=1)
            print('[AUTH] Проверка существования пользователя в базе [x]')
        else:
            print("User doesn`t exist!")

    def test_login_url(self):
        print('[AUTH] Проверка url логина []')
        login_url = '/auth/login/'
        self.assertEqual(settings.LOGIN_URL, login_url)
        print('[AUTH] Проверка url логина [x]')
    
    def test_login_request(self):
        print('[AUTH] Проверка входа пользователя в аккаунт []')
        login_url = settings.LOGIN_URL
        data = {
            'username': self.basic_user,
            'password': self.basic_user_password,
        }
        response = c.post(login_url, data, follow=True)
        response_status = response.status_code
        self.assertEqual(response_status, 200)
        print('[AUTH] Проверка входа пользователя в аккаунт [x]')
    
    def test_logout(self):
        print('[AUTH] Проверка выхода пользователя из аккаунта []')
        c.logout()
        response = c.get('/')
        self.assertTrue(response.status_code == 200)
        print('[AUTH] Проверка выхода пользователя из аккаунта [x]')
    
    def test_userpage_url(self):
        print('[AUTH] Проверка url userpage []')
        login_admin = c.login(username='admin', password='123')
        response = c.get('/auth/profile/')
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url userpage [x]')

    def test_customization_form(self):
        print('[AUTH] Проверка формы кастомизации на валидность []')
        
        # Передаём в форму тему и акцентный цвет и проверяем валидные в ней данные или нет
        form_valid = UserCustomizationForm(data={
            'theme': 'dark',
            'accent_color': 'green'
        })
        self.assertTrue(form_valid.is_valid())
        invalid_form = UserCustomizationForm(data={})
        self.assertEqual(bool(invalid_form.is_valid()), False)

        print('[AUTH] Проверка формы кастомизации на валидность [x]')
    
    def test_profilepic(self):
        print('[AUTH] Проверка смены аватара у пользователя []')
        profile_url = '/auth/profile/'
        image_profile = create_image('test_tmp.png')
        image_profile_file = SimpleUploadedFile('test_temp_image.png', image_profile.getvalue())
        # SimpleUploadedFile создаёт простое представление файла, у которого есть только размер, имя и его содержимое
        data = {'image': image_profile_file}
        c.login(username='admin', password='123')
        response = c.post(profile_url, data)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка смены аватара у пользователя [х]')
