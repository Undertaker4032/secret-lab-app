from django.contrib import admin
from .models import DocumentType, Documentation

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'created_date', 'required_clearance')
    list_filter = ('author', 'type', 'created_date', 'required_clearance')
    search_fields = ('title', 'content')
    readonly_fields = ('created_date', 'updated_date')
    date_hierarchy = 'created_date'
    
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