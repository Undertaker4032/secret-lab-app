from django.contrib import admin
from django.utils.html import format_html
from .models import DocumentType, Documentation

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'clickable_title', 'type', 'author', 'created_date', 'required_clearance', 'content_preview')
    list_display_links = ('clickable_title',)
    list_filter = ('type', 'required_clearance', 'created_date')
    search_fields = ('title', 'content', 'author__name')
    readonly_fields = ('created_date', 'updated_date')
    date_hierarchy = 'created_date'
    list_select_related = ('type', 'author', 'required_clearance')
    raw_id_fields = ('author', 'type', 'required_clearance')
    
    fieldsets = (
        (None, {
            'fields': ('title', 'type', 'content')
        }),
        ('Метаданные', {
            'fields': ('author', 'required_clearance')
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
    
    def content_preview(self, obj):
        preview = obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
        return format_html('<span title="{}">{}</span>', obj.content, preview)
    content_preview.short_description = 'Превью содержания'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'type', 'author', 'required_clearance'
        )