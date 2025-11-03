from django.contrib import admin
from .models import DocumentType, Documentation

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Documentation)
class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'author', 'created_date', 'required_clearance')
    list_filter = ('type', 'created_date', 'required_clearance', 'author')
    search_fields = ('title', 'content', 'author__name')
    readonly_fields = ('created_date', 'updated_date')
    date_hierarchy = 'created_date'
    list_select_related = ('type', 'author', 'required_clearance')
    
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
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'type', 'author', 'required_clearance'
        )