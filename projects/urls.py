from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('<int:pk>/complete/', views.complete_project, name='complete_project'),
    path('<int:pk>/toggle-participate/', views.toggle_participate, name='toggle_participate'),
]
