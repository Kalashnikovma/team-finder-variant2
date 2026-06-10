from django.db import models
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=6, choices=[("open", "Открыт"), ("closed", "Закрыт")], default="open")
    participants = models.ManyToManyField(User, related_name='participated_projects', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
