from django.urls import path
from django.contrib.auth import views as auth_views


from .views import (
    ProfileView,
    LogoutView,
    RegistrationView,
    LoginView,
    activate
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),

    path('login/', LoginView.as_view(), name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('activate-user/<uidb64>/<token>', activate, name='activate'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='authenticate/reset_password/reset_password.html',
                                                                 html_email_template_name='authenticate/reset_password/reset_password_email.html'),
                                                                 name="password_reset"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='authenticate/reset_password/reset_password_done.html'), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authenticate/reset_password/reset_password_confirm.html'),name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authenticate/reset_password/reset_password_complete.html'),name="password_reset_complete"),
]
