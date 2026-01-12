from django.contrib import admin
from .models import QA, Document, DocumentChunk, ChatBotConfig


@admin.register(QA)
class QAAdmin(admin.ModelAdmin):
    list_display = ('question',)
    search_fields = ('question',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'file_type', 'status', 'uploaded_at', 'processed_at')
    list_filter = ('file_type', 'status', 'uploaded_at')
    search_fields = ('original_filename',)
    readonly_fields = ('uploaded_at', 'processed_at', 'error_message')
    actions = ['process_documents']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file', 'original_filename', 'file_type')
        }),
        ('Processing Status', {
            'fields': ('status', 'error_message', 'uploaded_at', 'processed_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change or 'file' in form.changed_data:
            # Process new files or if file changed
            obj.process()

    @admin.action(description='Process selected documents')
    def process_documents(self, request, queryset):
        for doc in queryset:
            doc.process()
        self.message_user(request, f'Processed {queryset.count()} documents.')


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index', 'chunk_preview')
    list_filter = ('document',)
    search_fields = ('chunk_text',)
    readonly_fields = ('document', 'chunk_index', 'chunk_text', 'embedding', 'metadata')
    
    def chunk_preview(self, obj):
        return obj.chunk_text[:100] + '...' if len(obj.chunk_text) > 100 else obj.chunk_text
    chunk_preview.short_description = 'Preview'
    
    def has_add_permission(self, request):
        return False  # Chunks are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Read-only


@admin.register(ChatBotConfig)
class ChatBotConfigAdmin(admin.ModelAdmin):
    list_display = ('updated_at', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('updated_at',)

    def has_add_permission(self, request):
        # Allow adding if no active config exists, or just let them add new ones that override
        return True
