from django.db import models
from employees.models import Employee, ClearanceLevel

# Модель Статус Исследования
class ResearchStatus(models.Model):
    name = models.CharField(max_length=50, verbose_name='Статус Исследования')

    class Meta:
        verbose_name = 'Статус Исследования'
        verbose_name_plural = 'Статусы Исследований'

    def __str__(self):
        return f"{self.name}"

# Модель Исследование
class Research(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название Исследования')
    status = models.ForeignKey(ResearchStatus, on_delete=models.PROTECT, verbose_name='Статус Исследования')
    content = models.TextField(verbose_name='Содержание Исследования')
    lead = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Руководитель Исследования")
    team = models.ManyToManyField(Employee, related_name='research_team', blank=True, verbose_name='Участники Исследования')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата Создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата Обновления')
    required_clearance = models.ForeignKey(ClearanceLevel, on_delete=models.PROTECT, verbose_name='Уровень Допуска')

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title} ({self.status.name})"