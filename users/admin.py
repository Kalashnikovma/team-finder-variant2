from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Skill, UserSkill


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Поля для отображения в списке
    list_display = ('username', 'email', 'name', 'surname', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Поля для редактирования
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('name', 'surname', 'about', 'phone', 'github_url', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля для создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'surname', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'email', 'name', 'surname')
    ordering = ('-date_joined',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'created_at')
    list_filter = ('skill',)
    search_fields = ('user__username', 'user__email', 'skill__name')
