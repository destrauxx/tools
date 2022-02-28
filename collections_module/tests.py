from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from authenticate.models import UserInfo
from .models import Collection
from notes.views import Note


User = get_user_model()
c = Client()

# a
class CollectionsTests(TestCase):

    def setUp(self):
        basic_user = User(username='admin', email='a@a.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('123')
        basic_user.save()
        basic_user_info.save()
        self.basic_user = basic_user
        self.basic_user_password = 'a'
        self.basic_user_email = 'a@a.com'

        self.create_collection_url = '/notes/collection/create_form/'
    
    def test_importing_models(self):
        print('[COLLECTIONS] Проверка импортирования моделей []')
        try:
            from authenticate.models import UserInfo
            from .models import Collection
            import_status = True
        except:
            import_status = False
        
        self.assertTrue(import_status, msg='Ошибка импортирования одной из моделей!')
        print('[COLLECTIONS] Проверка импортирования моделей [x]')

    def test_check_urls(self):
        print('[COLLECTIONS] Проверка urls коллекции []')
        c.login(username='admin', password='123')

        col = Collection.objects.create(name='test col')
        col.save()
        note = Note.objects.create(header='header', text='text')
        note.save()

        response1 = c.get(self.create_collection_url, follow=True)
        response2 = c.get(f'/notes/collection/{col.id}/edit/', follow=True)
        response3 = c.get(f'/notes/collection/{col.id}/delete/', follow=True)
        response4 = c.get(f'/notes/collection/{col.id}/add_note/{note.id}/', follow=True)

        self.assertTrue(response1.status_code == 200)
        self.assertTrue(response2.status_code == 200)
        self.assertTrue(response3.status_code == 200)
        self.assertTrue(response4.status_code == 200)
        print('[COLLECTIONS] Проверка urls создания, изменения, удаления коллекции []')

    def test_create_edit_collection(self):
        print('[COLLECTIONS] Проверка создания, изменения коллекции []')
        c.login(username='admin', password='123')
        data = {
            'name': 'qwerty',
        }
        old_col_count = Collection.objects.all().count()

        # Тестирование создания
        response = c.post(self.create_collection_url, data)
        col_count = Collection.objects.all().count()

        self.assertEqual(old_col_count+1, col_count)
        self.assertEqual(response.status_code, 302)
        
        # Тестирование редактирования
        col = Collection.objects.get(id=1)
        edit_data = {
            'name': 'qwerty123',
        }
        response = c.post(f'/notes/collection/{col.id}/edit/', edit_data, follow=True)
        col = Collection.objects.get(id=1)

        self.assertEqual(col.name, 'qwerty123')
        self.assertEqual(response.status_code, 200)
        print('[COLLECTIONS] Проверка создания, изменения коллекции [x]')
