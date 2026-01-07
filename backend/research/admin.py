from django.contrib import admin
from .models import ResearchStatus, Research

@admin.register(ResearchStatus)
class ResearchStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'lead', 'status', 'created_date', 'required_clearance')
    list_filter = ('status', 'created_date', 'required_clearance', 'lead')
    search_fields = ('title', 'content', 'lead__name')
    readonly_fields = ('created_date', 'updated_date')
    filter_horizontal = ('team',)
    date_hierarchy = 'created_date'
    list_select_related = ('lead', 'status', 'required_clearance')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
        ('Команда и статус', {
            'fields': ('lead', 'team', 'status')
        }),
        ('Сроки и доступ', {
            'fields': ('created_date', 'updated_date', 'required_clearance')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'lead', 'status', 'required_clearance'
        ).prefetch_related('team')