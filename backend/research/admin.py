from django.contrib import admin
from django.utils.html import format_html
from .models import ResearchStatus, Research

@admin.register(ResearchStatus)
class ResearchStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'clickable_title', 'lead', 'status_badge', 'created_date', 'required_clearance', 'team_count')
    list_display_links = ('clickable_title',)
    list_filter = ('status', 'required_clearance', 'created_date')
    search_fields = ('title', 'content', 'lead__name')
    readonly_fields = ('created_date', 'updated_date')
    filter_horizontal = ('team',)
    date_hierarchy = 'created_date'
    list_select_related = ('lead', 'status', 'required_clearance')
    raw_id_fields = ('lead', 'status', 'required_clearance')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content')
        }),
        ('Команда и статус', {
            'fields': ('lead', 'team', 'status')
        }),
        ('Доступ', {
            'fields': ('required_clearance',)
        }),
        ('Даты', {
            'fields': ('created_date', 'updated_date'),
            'classes': ('collapse',)
        }),
    )
    
    def clickable_title(self, obj):
        return format_html('<strong>{}</strong>', obj.title)
    clickable_title.short_description = 'Название'
    clickable_title.admin_order_field = 'title'
    
    def status_badge(self, obj):
        colors = {
            'Завершено': 'green',
            'В процессе': 'blue',
            'Планируется': 'gray',
            'Приостановлено': 'orange',
        }
        color = colors.get(obj.status.name, 'black')
        return format_html('<span style="color: {};">● {}</span>', color, obj.status.name)
    status_badge.short_description = 'Статус'
    status_badge.admin_order_field = 'status__name'
    
    def team_count(self, obj):
        count = obj.team.count()
        return format_html('<span title="{} участников">{}</span>', count, count)
    team_count.short_description = 'Участники'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'lead', 'status', 'required_clearance'
        ).prefetch_related('team')