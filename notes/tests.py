from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from authenticate.models import UserInfo


User = get_user_model()
c = Client()

class NotesTest(TestCase):

    def setUp(self):
        basic_user = User(username='admin', email='a@a.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('123')
        basic_user.save()
        basic_user_info.save()
        self.basic_user = basic_user
        self.basic_user_password = 'a'
        self.basic_user_email = 'a@a.com'

        self.create_url = '/notes/create/'
        self.read_url = '/notes/read/'
        self.edit_url = '/notes/edit/'
        self.delete_url = '/notes/delete/'

    def test_importing_model(self):
        print('[NOTES] Проверка импортирования моделей')
        try:
            from authenticate.models import UserInfo
            from .models import Note
            import_status = True
        except:
            import_status = False
        
        self.assertTrue(import_status, msg='Ошибка импортирования одной из моделей!')

    def test_notes_urls(self):
        print('[NOTES] Проверка всех url заметок')
        c.login(username='admin', password='123')

        from .models import Note
        note = Note.objects.create()

        response = c.get(self.read_url)
        self.assertEqual(response.status_code, 200, msg='Страница read недоступна!')

        response = c.get(self.create_url)
        self.assertEqual(response.status_code, 200, msg='Страница create недоступна!')


        response = c.get(self.edit_url + f'{note.id}/')
        self.assertEqual(response.status_code, 200, msg='Страница edit недоступна!')

        response = c.get(self.delete_url + f'{note.id}/')
        self.assertEqual(response.status_code, 200, msg='Страница delete недоступна!')

    def test_CUD_notes(self):
        print('[NOTES] Проверка создания, удаления, редактирования заметки')

        c.login(username='admin', password='123')
        data = {
            'header': 'test note',
            'text': 'test note',
        }
        from .models import Note
        old_notes_count = Note.objects.all().count()

        # Тестирование создания
        response = c.post(self.create_url, data)
        notes_count = Note.objects.all().count()

        self.assertEqual(old_notes_count+1, notes_count, msg='Создание заметки провалено!')
        self.assertEqual(response.status_code, 302, msg='Перенаправление после создания заметки провалено')
        
        # Тестирование редактирования
        note = Note.objects.get(id=1)
        edit_data = {
            'header': 'new header',
            'text': 'new text',
        }
        response = c.post(self.edit_url + f'{note.id}/', edit_data)
        note = Note.objects.get(id=1)

        self.assertEqual(note.header, 'new header', msg='Название заметки не меняется при редактировании!')
        self.assertEqual(note.text, 'new text', msg='Текст заметки не меняется при редактировании!')
        self.assertEqual(response.status_code, 302, msg='Перенаправление после редактирования заметки провалено')

        
        # Тестирование удаления
        response = c.post(self.delete_url + f'{note.id}/')
        notes_count = Note.objects.all().count()

        self.assertEqual(old_notes_count, notes_count, msg='Удаление заметки провалено')
        self.assertEqual(response.status_code, 302, msg='Перенаправление после удаления заметки провалено')
