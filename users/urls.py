from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('<int:user_id>/', views.user_profile, name='profile'),
    path('ajax/search-skills/', views.search_skills, name='search_skills'),
    path('ajax/add-skill/', views.add_skill, name='add_skill'),
    path('ajax/remove-skill/<int:user_skill_id>/', views.remove_skill, name='remove_skill'),
]
