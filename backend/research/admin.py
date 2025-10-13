from django.contrib import admin
from .models import ResearchStatus, Research

@admin.register(ResearchStatus)
class ResearchStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'lead', 'status', 'created_date', 'required_clearance')
    list_filter = ('lead', 'status', 'created_date', 'required_clearance')
    search_fields = ('title', 'description', 'objectives')
    readonly_fields = ('created_date', 'updated_date')
    filter_horizontal = ('team',)
    date_hierarchy = 'created_date'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'objectives')
        }),
        ('Команда и статус', {
            'fields': ('lead', 'team', 'status')
        }),
        ('Сроки и доступ', {
            'fields': ('created_date', 'updated_date', 'required_clearance')
        }),
        ('Результаты', {
            'fields': ('findings',),
            'classes': ('collapse',)
        }),
    )