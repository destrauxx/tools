from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserInfo(models.Model): # Модель, содержащая параметры кастомизации и аватар пользователя
    class ChooseAccentColor(models.TextChoices):
        RED = 'red'
        GREEN = 'green'
        ORANGE = 'orange'
        LIGHT_BLUE = 'light_blue'
    class ChooseTheme(models.TextChoices):
        LIGHT = 'light'
        DARK = 'dark'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(
        max_length=5,
        choices=ChooseTheme.choices,
        default='light')
    accent_color = models.CharField(
        max_length=10,
        choices=ChooseAccentColor.choices,
        default='green')
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    def change_theme(self, theme): # Меняет тему на переданный черезе аргумент theme
        self.theme = theme

    def change_accent_color(self, accent_color): # Меняет акцентный цвет на переданный через аргумент accent_color
        self.accent_color = accent_color

    def __str__(self): # При конвертации модели в строку возвращает имя пользователя
        return self.user.username