from email import message
import re
from datetime import datetime, timezone
from time import time
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.core.mail import EmailMessage

from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
from .forms import RegisterForm, UpdateProfileImageForm, UserCustomizationForm
from notes.models import Collection, Note
from .models import UserInfo

def activate(request, uidb64, token):
    '''
        Активирует пользователя, если будет найден пользователь и его токен будет верен
    '''
    try:
        # Декодируем id пользователя из base64 в байты, далее в текст
        uid = force_text(urlsafe_base64_decode(uidb64))
        # Проверяем, есть ли пользователь с таким id и присваеваем в переменную user
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        # В случае ошибки присваеваем к user значение None
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        # Если переменная user содержит пользователя и токен ссылки присвоен пользователю,
        # то user становится активным и сохраняется 
        user.is_active = True
        user.save()
        return render(request, 'authenticate/email_verification/email_verification_complete.html')
    else:
        # Если пользователя нет или токен ссылки не валиден
        return HttpResponse('Activation link is invalid!')

class RegistrationView(CreateView):
    template_name = 'authenticate/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm

    def form_valid(self, form):
        # Получение данных из формы,
        # создание пользователя и модели его сведений
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        user_info = UserInfo(user=user)
        user_info.save()

        # Получение почты пользователя, сайта
        # Отправка письма верификации на почту с доменом сайта
        email = form.cleaned_data.get('email')
        current_site = get_current_site(self.request)
        email_subject = 'Please, verificate your email'
        verificate_message = render_to_string('authenticate/email_verification/email_verification_body.html', {
                                    'domain':current_site.domain,
                                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token':account_activation_token.make_token(user),
                                    })
        email_adress = EmailMessage(email_subject, verificate_message, to=[email])
        email_adress.content_subtype = "html"
        email_adress.send()
        messages.add_message(self.request, messages.WARNING, f'We sent email to verify your account on {email}')
        return redirect('/auth/login')
    

class LoginView(LoginView):
    template_name = 'authenticate/login.html'
    success_url = reverse_lazy('homepage')

class LogoutView(LogoutView):
    redirect_field_name = reverse_lazy("homepage")
    template_name = "index.html"

class ProfileView(DetailView, FormView):
    template_name = "authenticate/profile.html"
    model = UserInfo
    # extra_context = {
    #     'form_update_image': UpdateProfileImageForm(),
    #     'form_customization': UserCustomizationForm(),
    #     'user': User.objects.get(username=request.user),

    # }

    def get(self, request, *args, **kwargs):
        form_update_image = UpdateProfileImageForm()
        form_customization = UserCustomizationForm()
        user = User.objects.get(username=request.user)
        # last_login = user.last_login.strftime('%d.%m.%y')
        now = datetime.now(timezone.utc)
        joined = (now - user.date_joined).days
        user_info = get_object_or_404(UserInfo, user=request.user)
        user_notes = Note.objects.filter(user=request.user)
        user_collections = Collection.objects.filter(user=request.user)
        
        return render(request, self.template_name, {'form_customization': form_customization,
                                                    'form_update_image': form_update_image,
                                                    'profile': request.user,
                                                    'user_info': user_info,
                                                    'user_notes': user_notes,
                                                    'user_collections': user_collections,
                                                    'joined': joined})

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = User.objects.get(username=self.request.user)

    #     context['user'] = user
    #     context['user_info'] = get_object_or_404(UserInfo, user=user)
    #     context['user_notes'] = Note.objects.filter(user=user)
    #     context['user_collections'] = Collection.objects.filter(user=user)
    #     context['last_login'] = user.last_login.strftime('%d.%m.%y')
    #     context['form_update_image'] = UpdateProfileImageForm()
    #     context['form_customization'] = UserCustomizationForm()
    #     return context

    def post(self, request, *args, **kwargs):
        form_update_image = UpdateProfileImageForm(request.POST, request.FILES)
        form_customization = UserCustomizationForm(request.POST)

        user = User.objects.get(username=request.user)
        last_login = user.last_login.strftime('%d.%m.%y')
        user_info = get_object_or_404(UserInfo, user=request.user)
        user_notes = Note.objects.filter(user=request.user)
        user_collections = Collection.objects.filter(user=request.user)

        if form_update_image.is_valid():
            new_image = form_update_image.cleaned_data['new_image']
            user_info.profile_image = new_image
            user_info.save()

        if form_customization.is_valid():
            new_theme = form_customization.cleaned_data['theme']
            new_accent_color = form_customization.cleaned_data['accent_color']
            user_info.theme = new_theme
            user_info.accent_color = new_accent_color
            user_info.save()
            
        return render(request, self.template_name, {'form_customization': form_customization,
                                                    'form_update_image': form_update_image,
                                                    'profile': request.user,
                                                    'user_info': user_info,
                                                    'user_notes': user_notes,
                                                    'user_collections': user_collections,
                                                    'last_login': last_login})
                                                    
