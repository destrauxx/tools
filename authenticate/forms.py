from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext as gettext

from .models import UserInfo
    
class RegisterForm(UserCreationForm): # Форма, используемая для регистрации пользователя
    username = UsernameField(label='') # Имя пользователя
    email = forms.EmailField(label='') # Почта пользователя
    password1 = forms.CharField(label='', 
                                widget=forms.PasswordInput) # Первый ввод пароля с виджетом PasswordInput
    password2 = forms.CharField(label='', 
                                widget=forms.PasswordInput) # Второй ввод пароля с виджетом PasswordInput

    error_messages = {
        'email_exists': gettext('Your email is already exists.'),
        'password_mismatch': gettext('The two password fields didn’t match.'),
    }
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'off',
            'autofill': 'None'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
            )
        else:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
            )
        else:
            return password2
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }
            
class UpdateProfileImageForm(forms.Form):
    new_image = forms.ImageField()

class UserCustomizationForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'theme',
            'accent_color'
        ]