from django.contrib.auth.backends import UserModel, ModelBackend
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs): 
        '''
        Аутентифицирует через settings.AUTH_USER_MODEL
        input:
            username - логин из формы, имя или почта пользователя.
            password - пароль из формы.
        output:
            user - пользователь
        '''
        try:
            # Пытаемся получить пользователя по имени или почте (Q позволяет использовать логические операторы, __iexact не чувствителен к регистру)
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            # Если пользователя нет, то создаем нового и присваиваем пароль из формы
            user = UserModel().set_password(password)
        except MultipleObjectsReturned:
            # Если пользователей несколько, сортируем по id (order_by) и берем первого .first()
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()
        else:
            # Если пользователь есть - проверка пароля пользователя user.check_password(password)
            # и проверка статуса is_active с помощью .user_can_authenticate(user)
            if user.check_password(password) and self.user_can_authenticate(user):
                # Если пароль подходит по стандартам и is_active = True - возвращаем пользователя
                return user
    
    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        
        if self.user_can_authenticate(user):
            return user
        else:
            return None