from django.contrib import admin
from .models import Cluster, Department, Division, Position, ClearanceLevel, Employee

# Простые модели без настроек
admin.site.register(Cluster)
admin.site.register(ClearanceLevel)

# Классы для более сложных моделей с настройками
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cluster')  # Поля, отображаемые в списке
    list_filter = ('cluster',)  # Фильтр по кластерам
    search_fields = ('name',)  # Поиск по названию

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'get_cluster')
    list_filter = ('department__cluster', 'department')
    search_fields = ('name', 'department__name')
    
    def get_cluster(self, obj):
        return obj.department.cluster
    get_cluster.short_description = 'Кластер'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'cluster')
    list_filter = ('cluster',)
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'division', 'clearance_level', 'get_cluster')
    list_filter = ('clearance_level', 'division__department__cluster', 'position')
    search_fields = ('name', 'user__username')
    readonly_fields = ('department', 'cluster')  # Вычисляемые поля только для чтения
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'clearance_level')
        }),
        ('Структура', {
            'fields': ('division', 'position', 'department', 'cluster')
        }),
        ('Дополнительно', {
            'fields': ('profile_picture',),
            'classes': ('collapse',)  # Сворачиваемый блок
        }),
    )
    
    def get_cluster(self, obj):
        return obj.cluster
    get_cluster.short_description = 'Кластер'
    
    def department(self, obj):
        return obj.department
    department.short_description = 'Департамент'