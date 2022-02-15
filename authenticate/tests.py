from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from PIL import Image
from io import BytesIO

from .tokens import account_activation_token

from .models import UserInfo
from .forms import UserCustomizationForm

User = get_user_model()
c = Client()

def create_image(filename, size=(70, 70), image_format="png", image_mode="RGB"):
    # создаём поток, использующий буфер байтов в памяти.
    data = BytesIO()
    # создаём картинку с заданным размером и форматом
    Image.new(image_mode, size).save(data, image_format)
    # Перемещает указатель текущей позиции в файле в его начало.
    data.seek(0)
    return data

class ProfileTest(TestCase):

    def setUp(self):
        # Создаем пользователя во временной базе данных
        basic_user = User(username='admin', email='a@a.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('123')
        basic_user.save()
        basic_user_info.save()
        self.basic_user = basic_user
        self.basic_user_password = 'a'
        self.basic_user_email = 'a@a.com'

    def test_importing_model(self):
        print('[AUTH] Проверка импортирования модели UserInfo')
        try:
            # Импортируем модель и ставим import_status = True
            from .models import UserInfo
            import_status = True
        except:
            # Если при импортировании модели произошла ошибка, то import_status = False
            import_status = False

        # Если import_status = True, то тест пройден, иначе msg
        self.assertTrue(import_status, msg='Модель UserInfo не импортирована!')

    def test_registration_url(self):
        print('[AUTH] Проверка url регистрации []')
        registration_url = '/auth/register/'
        # Посылаем get запрос на указанный url
        response = c.get(registration_url)
        # Если статус запроса 200, то тест пройден, иначе msg
        self.assertEqual(response.status_code, 200, msg='URL регистрации недоступен!')

    def test_registration_request(self):
        print('[AUTH] Проверка регистрации пользователя')
        registration_url = '/auth/register/'

        # Данные, используемые при регистрации
        data = {
            'username': 'user',
            'email': 'a@a.com',
            'password1': 'Abcdefg404',
            'password2': 'Abcdefg404',
        }

        # Посылаем post запрос на url регистрации с данными
        response = c.post(registration_url, data, follow=True)
        self.assertEqual(response.status_code, 200, msg='Регистрация не пройдена!')
    

    def test_login_url(self):
        print('[AUTH] Проверка url логина')
        login_url = settings.LOGIN_URL
        # Посылаем get запрос на указанный url
        response = c.get(login_url)
        self.assertEqual(response.status_code, 200, msg='URL логина недоступен!')
    
    def test_login_request(self):
        print('[AUTH] Проверка входа пользователя в аккаунт')
        login_url = settings.LOGIN_URL
        # Данные запроса
        data = {
            'username': self.basic_user,
            'password': self.basic_user_password,
        }
        # Запрос на url логина с данными
        response = c.post(login_url, data, follow=True)
        self.assertEqual(response.status_code, 200, msg='Логин не пройден!')
    
    def test_logout(self):
        print('[AUTH] Проверка выхода пользователя из аккаунта')
        logout_url = '/auth/logout/'
        response = c.post(logout_url)
        self.assertTrue(response.status_code == 302)
        
    def test_userpage_url(self):
        print('[AUTH] Проверка url userpage')
        login_admin = c.login(username='admin', password='123')
        response = c.get('/auth/profile/')
        self.assertEqual(response.status_code, 200)

    def test_customization_form(self):
        print('[AUTH] Проверка формы кастомизации на валидность []')
        # Передаём в форму тему и акцентный цвет и проверяем валидные в ней данные или нет
        c.login(username='admin', password='123')
        url = "/auth/profile/"
        data = {
            'theme': 'light',
            'accent_color': 'orange'
        }
        response = c.post(url, data)
        form_valid = UserCustomizationForm(data={
            'theme': 'dark',
            'accent_color': 'green'
        })
        self.assertTrue(form_valid.is_valid())
        invalid_form = UserCustomizationForm(data={})
        self.assertEqual(bool(invalid_form.is_valid()), False)
        self.assertTrue(response.status_code == 200)

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

    def test_reset_password_url(self):
        print('[AUTH] Проверка url reset_password []')
        url = "/auth/reset_password/"
        response = c.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url reset_password [x]')
    
    def test_reset_password_form(self):
        print('[AUTH] Проверка формы reset_password []')
        url = "/auth/reset_password/"
        data = {
            'email': 'a@a.com'
        }
        response = c.post(url, data, follow=True)
        form_valid = PasswordResetForm(data={
            'email': 'a@a.com'
        })
        form_invalid = PasswordResetForm(data={
            'email': ''
        })
        self.assertTrue(form_valid.is_valid())
        self.assertFalse(form_invalid.is_valid())
        self.assertTrue(response.status_code == 200)
        print('[AUTH] Проверка формы reset_password [x]')
    
    def test_reset_password_sent_url(self):
        print('[AUTH] Проверка url reset_password_sent []')
        url = '/auth/reset_password_sent/'
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url reset_password_sent [x]')

    def test_reset_password_confirm_url(self):
        print('[AUTH] Проверка url reset_password_confirm []')
        user = User.objects.get(pk=1)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url = f"/auth/reset/<{uidb64}>/<{token}/"
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url reset_password_confirm [x]')
    
    def test_reset_password_confirm_form_valid(self):
        print('[AUTH] Проверка формы reset_password_confirm []')
        user = User.objects.get(pk=1)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url = f"/auth/reset/<{uidb64}>/<{token}/"
        data = {
            'new_password1': 'lmznxbcv',
            'new_password2': 'lmznxbcv'
        }
        form_valid = SetPasswordForm(user=user, data={
            'new_password1': 'lmznxbcv',
            'new_password2': 'lmznxbcv'
        })
        form_invalid = SetPasswordForm(user=user, data={
            'new_password1': '',
            'new_password2': 'a'
        })
        response = c.post(url, data, follow=True)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(form_valid.is_valid())
        self.assertFalse(form_invalid.is_valid())
        print('[AUTH] Проверка формы reset_password_confirm [x]')
    
    def test_reset_password_complete_url(self):
        print('[AUTH] Проверка url reset_password_complete []')
        url = "/auth/reset_password_complete/"
        response = c.get(url)
        self.assertTrue(response.status_code == 200)
        print('[AUTH] Проверка url reset_password_complete [x]')

    def test_verification_url_valid(self):
        print('[AUTH] Проверка url верификации []')
        user = User.objects.get(pk=1)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        url = "/auth/activate-user/<{uidb64}>/<{token}>"
        response = c.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        print('[AUTH] Проверка url верификации [x]')