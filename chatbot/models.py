from django.db import models
from django.utils import timezone
import json
import os
from .utils import extract_text_from_file, chunk_text, generate_embedding
from .utils import extract_text_from_file, chunk_text, generate_embedding

class QA(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Document(models.Model):
    """Stores uploaded documents for RAG"""
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('txt', 'Text'),
        ('docx', 'Word Document'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    file = models.FileField(upload_to='chatbot_documents/')
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} ({self.get_file_type_display()})"

    def save(self, *args, **kwargs):
        if self.file:
            if not self.original_filename:
                self.original_filename = self.file.name
            if not self.file_type:
                filename = self.file.name.lower()
                if filename.endswith('.pdf'):
                    self.file_type = 'pdf'
                elif filename.endswith('.txt'):
                    self.file_type = 'txt'
                elif filename.endswith('.docx'):
                    self.file_type = 'docx'
        super().save(*args, **kwargs)

    def process(self):
        """Extract text, chunk, and generate embeddings"""
        try:
            self.status = 'processing'
            self.save()
            
            # Extract text
            text = extract_text_from_file(self.file.path, self.file_type)
            
            if not text.strip():
                self.status = 'failed'
                self.error_message = 'No text extractable'
                self.save()
                return

            # Clear existing chunks
            self.chunks.all().delete()
            
            # Chunk text
            chunks = chunk_text(text)
            
            # Get API key
            config = ChatBotConfig.objects.filter(is_active=True).last()
            if not config or not config.gemini_api_key:
                raise ValueError("Gemini API key not configured in Admin Panel")
            
            api_key = config.gemini_api_key

            # Generate embeddings and save
            for idx, c_text in enumerate(chunks):
                embedding = generate_embedding(c_text, api_key)
                DocumentChunk.objects.create(
                    document=self,
                    chunk_text=c_text,
                    chunk_index=idx,
                    embedding=json.dumps(embedding)
                )

            self.status = 'completed'
            self.processed_at = timezone.now()
            self.error_message = ''
            self.save()

        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            self.save()


class DocumentChunk(models.Model):
    """Stores text chunks with embeddings for semantic search"""
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_text = models.TextField()
    chunk_index = models.IntegerField()
    embedding = models.TextField()  # JSON array of floats
    metadata = models.JSONField(default=dict, blank=True)  # page number, section, etc.
    
    class Meta:
        ordering = ['document', 'chunk_index']
        unique_together = ['document', 'chunk_index']
    
    def __str__(self):
        return f"{self.document.original_filename} - Chunk {self.chunk_index}"
    
    def set_embedding(self, embedding_list):
        """Store embedding as JSON string"""
        self.embedding = json.dumps(embedding_list)
    
    def get_embedding(self):
        """Retrieve embedding as list"""
        return json.loads(self.embedding) if self.embedding else []


class ChatBotConfig(models.Model):
    """Configuration for Chatbot settings"""
    gemini_api_key = models.CharField(max_length=255, help_text="Enter your Gemini API Key")
    is_active = models.BooleanField(default=True, help_text="Only the most recently updated active config will be used")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chatbot Configuration"
        verbose_name_plural = "Chatbot Configuration"

    def __str__(self):
        return f"Config updated at {self.updated_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other configs
            ChatBotConfig.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
