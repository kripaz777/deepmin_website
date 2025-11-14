from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='DeepMinds')
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    hero_video = models.FileField(upload_to='hero/', null=True, blank=True)
    hero_phrases = models.TextField(default='Develop, Operate & Deploy AI You Can Trust at Scale\nTurn Data into High-Value AI Outcomes')

    def __str__(self):
        return 'Site Settings'

class Service(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    icon_class = models.CharField(max_length=80, blank=True)
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='projects/', null=True, blank=True)
    category = models.CharField(max_length=80, blank=True)
    short_description = models.TextField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return self.title

class Training(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    duration = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=100, blank=True)
    content = RichTextUploadingField(blank=True, null=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True)
    content = RichTextUploadingField()
    cover_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)
    def __str__(self): return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/', null=True, blank=True)
    bio = models.TextField(blank=True)
    def __str__(self): return self.name

class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    def __str__(self): return f"{self.author} - {self.company}"

class Industry(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='industries/', null=True, blank=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='products/', null=True, blank=True)
    link = models.URLField(blank=True)
    def __str__(self): return self.name

class ResearchItem(models.Model):
    title = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    link = models.URLField(blank=True)
    def __str__(self): return self.title

class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    remote = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    posted_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return self.title

class Application(models.Model):
    job = models.ForeignKey(JobOpening, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    cover_message = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/')
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return f"{self.name} - {self.job or 'General'}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=250, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return f"{self.name} - {self.subject}"
