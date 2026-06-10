from django.db import models
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание проекта")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_projects',
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, verbose_name="Ссылка на GitHub")
    status = models.CharField(
        max_length=6,
        choices=[("open", "Открыт"), ("closed", "Закрыт")],
        default="open",
        verbose_name="Статус"
    )
    participants = models.ManyToManyField(
        User, 
        related_name='participated_projects', 
        blank=True,
        verbose_name="Участники"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
