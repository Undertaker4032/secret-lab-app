from django.contrib import admin
from django.utils.html import format_html
from .models import Cluster, Department, Division, Position, ClearanceLevel, Employee

@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(ClearanceLevel)
class ClearanceLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'name')
    list_display_links = ('number',)
    search_fields = ('number',)
    ordering = ('number',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cluster')
    list_display_links = ('name',)
    list_filter = ('cluster',)
    search_fields = ('name', 'cluster__name')
    list_select_related = ('cluster',)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department', 'get_cluster')
    list_display_links = ('name',)
    list_filter = ('department__cluster', 'department')
    search_fields = ('name', 'department__name', 'department__cluster__name')
    list_select_related = ('department__cluster',)
    
    def get_cluster(self, obj):
        return obj.department.cluster
    get_cluster.short_description = 'Кластер'
    get_cluster.admin_order_field = 'department__cluster'

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cluster')
    list_display_links = ('name',)
    list_filter = ('cluster',)
    search_fields = ('name', 'cluster__name')
    list_select_related = ('cluster',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'clickable_name', 'is_active_badge', 'position', 'division', 'clearance_level', 'get_cluster')
    list_display_links = ('clickable_name',)
    list_filter = ('is_active', 'clearance_level', 'division__department__cluster', 'position', 'division')
    search_fields = ('name', 'user__username', 'user__email', 'division__name')
    readonly_fields = ('get_department', 'get_cluster', 'user_link')
    list_select_related = ('position', 'division__department__cluster', 'clearance_level', 'user')
    raw_id_fields = ('user', 'division', 'position', 'clearance_level')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'is_active', 'clearance_level')
        }),
        ('Структура', {
            'fields': ('division', 'position', 'get_department', 'get_cluster')
        }),
        ('Дополнительно', {
            'fields': ('profile_picture', 'user_link'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_employees', 'deactivate_employees']
    
    def clickable_name(self, obj):
        return format_html('<strong>{}</strong>', obj.name)
    clickable_name.short_description = 'Имя'
    clickable_name.admin_order_field = 'name'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">● Активен</span>')
        return format_html('<span style="color: red;">● Неактивен</span>')
    is_active_badge.short_description = 'Статус'
    is_active_badge.admin_order_field = 'is_active'
    
    def get_cluster(self, obj):
        return obj.cluster
    get_cluster.short_description = 'Кластер'
    get_cluster.admin_order_field = 'division__department__cluster'
    
    def get_department(self, obj):
        return obj.department
    get_department.short_description = 'Департамент'
    
    def user_link(self, obj):
        if obj.user and obj.user.id:
            url = f"/admin/auth/user/{obj.user.id}/change/"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = 'Пользователь'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'division__department__cluster',
            'position',
            'clearance_level',
            'user'
        )
    
    def activate_employees(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} сотрудников активировано')
    activate_employees.short_description = "Активировать выбранных"
    
    def deactivate_employees(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} сотрудников деактивировано')
    deactivate_employees.short_description = "Деактивировать выбранных"