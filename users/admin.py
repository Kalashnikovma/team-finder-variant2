from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Skill, UserSkill


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'surname', 'is_staff')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('name', 'surname', 'avatar', 'phone', 'github_url', 'about')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'password1', 'password2')}),
    )


admin.site.register(Skill)
admin.site.register(UserSkill)
