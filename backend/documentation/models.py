from django.db import models
from employees.models import Employee, ClearanceLevel

# Модель Тип Документа
class DocumentType(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тип Документа')

    class Meta:
        verbose_name = 'Тип Документа'
        verbose_name_plural = 'Типы Документов'

    def __str__(self):
        return f"{self.name}"

# Модель Документ
class Documentation(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название Документа')
    type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, verbose_name='Тип Документа')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(Employee, on_delete=models.PROTECT, verbose_name="Автор")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата Создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата Обновления')
    required_clearance = models.ForeignKey(ClearanceLevel, on_delete=models.PROTECT, verbose_name='Уровень Допуска')
    is_confidentional = models.BooleanField(default=False, verbose_name='Конфиденциальный')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title} ({self.type.name})"