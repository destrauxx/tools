from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from notes.views import HomePageView

from django_email_verification import urls as email_urls 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='homepage'),
    path('auth/', include('authenticate.urls')),
    path('notes/', include('notes.urls')),
    path('notes/', include('collections_module.urls')),
    path('email/', include(email_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
