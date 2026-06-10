from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница — редирект на список проектов
    path('', lambda request: redirect('project_list'), name='home'),
    
    # Приложения
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls')),
]

# Для отображения медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
