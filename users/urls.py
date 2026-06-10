from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('list/', views.user_list, name='user_list'),
    path('<int:pk>/', views.user_detail, name='user_detail'),
    path('<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Навыки (Вариант 2)
    path('skills/', views.skill_autocomplete, name='skill_autocomplete'),
    path('<int:pk>/skills/add/', views.add_skill, name='add_skill'),
    path('<int:pk>/skills/<int:skill_id>/remove/', views.remove_skill, name='remove_skill'),
]
