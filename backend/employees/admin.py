from django.contrib import admin
from .models import Cluster, Department, Division, Position, ClearanceLevel, Employee

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ClearanceLevel)
class ClearanceLevelAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
    search_fields = ('number',)
    ordering = ('number',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'cluster')
    list_filter = ('cluster',)
    search_fields = ('name', 'cluster__name')
    list_select_related = ('cluster',)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'get_cluster')
    list_filter = ('department__cluster', 'department')
    search_fields = ('name', 'department__name', 'department__cluster__name')
    list_select_related = ('department__cluster',)
    
    def get_cluster(self, obj):
        return obj.department.cluster
    get_cluster.short_description = 'Кластер'
    get_cluster.admin_order_field = 'department__cluster'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'cluster')
    list_filter = ('cluster',)
    search_fields = ('name', 'cluster__name')
    list_select_related = ('cluster',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'position', 'division', 'clearance_level', 'get_cluster')
    list_filter = ('is_active', 'clearance_level', 'division__department__cluster', 'position', 'division')
    search_fields = ('name', 'user__username', 'division__name')
    readonly_fields = ('get_department', 'get_cluster')
    list_select_related = ('position', 'division__department__cluster', 'clearance_level')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'is_active', 'clearance_level')
        }),
        ('Структура', {
            'fields': ('division', 'position', 'get_department', 'get_cluster')
        }),
        ('Дополнительно', {
            'fields': ('profile_picture',),
            'classes': ('collapse',)
        }),
    )
    
    def get_cluster(self, obj):
        return obj.cluster
    get_cluster.short_description = 'Кластер'
    get_cluster.admin_order_field = 'division__department__cluster'
    
    def get_department(self, obj):
        return obj.department
    get_department.short_description = 'Департамент'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'division__department__cluster',
            'position',
            'clearance_level'
        )