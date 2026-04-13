from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # 🔹 Главная страница перенаправляет на список проектов
    path("", RedirectView.as_view(url="/projects/", permanent=False)),
    # 🔹 Маршруты аутентификации на корневом уровне
    path("register/", users_views.register_view, name="register"),
    path("login/", users_views.login_view, name="login"),
    path("logout/", users_views.logout_view, name="logout"),
    # 🔹 Подключение приложений
    path("users/", include("users.urls", namespace="users")),
    path("projects/", include("projects.urls", namespace="projects")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
