from django.test import TestCase, Client

from django.contrib.auth import get_user_model

from authenticate.models import UserInfo
from .models import Note

User = get_user_model()
c = Client()

class NotesTest(TestCase):

    def setUp(self):
        basic_user = User(username='user', email='user@google.com')
        basic_user_info = UserInfo(user=basic_user)
        basic_user.set_password('user')
        basic_user.save()
        self.basic_user = basic_user

    def test_creating_note(self):
        print('[NOTES] Проверка создания заметки []')

        old_notes_count = Note.objects.count()
        new_note = Note.objects.create(user=self.basic_user,
                                       header='Test note', 
                                       text='Test note text')
        notes_count = Note.objects.count()

        self.assertFalse(old_notes_count == notes_count, msg='Ошибка создания заметки')
        print('[NOTES] Проверка создания заметки [х]')

    def test_deleting_notes(self):
        print('[NOTES] Проверка удаления заметки []')

        note = Note.objects.create(user=self.basic_user,
                                       header='Test note', 
                                       text='Test note text')
        old_notes_count = Note.objects.count()
        note.delete()
        notes_count = Note.objects.count()

        self.assertFalse(old_notes_count == notes_count, msg='Ошибка удаления заметки')
        print('[NOTES] Проверка удаления заметки [x]')