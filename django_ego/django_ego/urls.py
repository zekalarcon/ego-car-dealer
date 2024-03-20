from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 
from cars import views

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/', include('login.urls')),
    path('api/v1/', include('cars.urls')),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
