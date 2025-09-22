from django.db import models
from django.contrib.auth.models import User

# Модель Кластер
class Cluster(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')

    class Meta:
        verbose_name = 'Кластер'
        verbose_name_plural = 'Кластеры'

    def __str__(self):
        return f"{self.name}"

# Модель Департамент
class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name='departments', verbose_name='Кластеры')

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        unique_together = ('name', 'cluster')
        indexes = [models.Index(fields=['cluster', 'name']),]

    def __str__(self):
        return f"{self.name} ({self.cluster.name})"
    
# Модель Подразделение
class Division(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='divisions', verbose_name='Подразделения')

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        unique_together = ('name', 'department')
        indexes = [models.Index(fields=['department', 'name']),]

    def __str__(self):
        return f"{self.name} ({self.department.name})"

# Модель Должность
class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE, related_name='positions', verbose_name='Кластеры')

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        unique_together = ('name', 'cluster')
        indexes = [models.Index(fields=['cluster', 'name']),]

    def __str__(self):
        return f"{self.name} ({self.cluster.name})"
        
# Модель Уровень Допуска
class ClearanceLevel(models.Model):
    number = models.IntegerField(default=0, unique=True, verbose_name='Уровень Допуска')
    
    class Meta:
        verbose_name = 'Уровень Допуска'
        verbose_name_plural = 'Уровни Допуска'

    @property
    def name(self):
        return f"{self.number}-У.Д."

    def __str__(self):
        return self.name
    
# Основная модель Сотрудник
class Employee(models.Model):
    # Связь с моделью User для аутентификации
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='Пользователь')
    name = models.CharField(max_length=100, on_delete=models.CASCADE, verbose_name='Имя и Фамилия')
    clearance_level = models.ForeignKey(ClearanceLevel, on_delete=models.SET_NULL, verbose_name='Уровень Допуска')
    division = models.ForeignKey(Division, on_delete=models.PROTECT, verbose_name='Подразделение')

    @property
    def department(self):
        return self.division.department
    
    @property
    def cluster(self):
        return self.division.department.cluster
    
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, verbose_name='Должность')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Фото')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f"{self.name} ({self.position})"