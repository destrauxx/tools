from django.test import TestCase, Client

from django.contrib.auth import get_user_model

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

    def test_importing_model(self):
        print('[AUTH] Проверка импортирования модели UserInfo []')
        try:
            from .models import UserInfo
            import_status = True
        except:
            import_status = False

        self.assertTrue(import_status, msg='Модель UserInfo не импортирована!')
        print('[AUTH] Проверка импортирования модели UserInfo [x]')
