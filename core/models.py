from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default='DeepMinds')
    logo = models.ImageField(upload_to='site/', null=True, blank=True)
    hero_video = models.FileField(upload_to='hero/', null=True, blank=True)
    hero_phrases = models.TextField(default='Develop, Operate & Deploy AI You Can Trust at Scale\nTurn Data into High-Value AI Outcomes')
    hero_title = models.CharField(max_length=250, default='Next-Gen AI Agents & Autonomous Systems')
    hero_subtitle = models.TextField(default='We architect intelligent ecosystems that think, learn, and execute. From agentic workflows to enterprise LLMs, we build the future of autonomy.')
    
    what_we_do_subtitle = models.CharField(max_length=100, default='What We Do')
    what_we_do_title = models.CharField(max_length=250, default='Comprehensive AI <span class="text-gradient">Solutions</span>')
    what_we_do_desc = models.TextField(default='End-to-end services to help you adopt and scale artificial intelligence with cutting-edge technology.')

    footer_text = models.TextField(default="We build dependable AI systems — research, productization, and production operations.", blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    copyright_text = models.CharField(max_length=200, default='© 2026 DeepMinds. All rights reserved.')

    # Contact Info
    contact_email = models.EmailField(default='hello@deepminds.academy')
    contact_phone = models.CharField(max_length=20, default='+977 98xxxxxxx')
    contact_address = models.CharField(max_length=255, default='Kathmandu, Nepal')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

class Service(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    icon_class = models.CharField(max_length=80, blank=True)
    order = models.PositiveIntegerField(default=0)
    def __str__(self): return self.title

class CoreValue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=80, blank=True, help_text="FontAwesome class, e.g., fas fa-microchip")
    image = models.ImageField(upload_to='values/', null=True, blank=True)
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
    LEVEL_CHOICES = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    summary = models.TextField()
    thumbnail = models.ImageField(upload_to='trainings/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    instructor_name = models.CharField(max_length=200, default='Expert Instructor')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    students_count = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    duration = models.CharField(max_length=100, blank=True)
    mode = models.CharField(max_length=100, blank=True, help_text='e.g., Online, In-person, Hybrid')
    category = models.CharField(max_length=100, default='General AI')
    content = RichTextUploadingField(blank=True, null=True, verbose_name="Detailed Syllabus")
    is_popular = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    def __str__(self): return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = RichTextUploadingField()
    cover_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            original_slug = slugify(self.title)
            queryset = BlogPost.objects.all().filter(slug__iexact=original_slug).count()

            count = 1
            slug = original_slug
            while(queryset):
                slug = original_slug + '-' + str(count)
                count += 1
                queryset = BlogPost.objects.all().filter(slug__iexact=slug).count()
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self): return self.title

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email

class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='team/', null=True, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
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
    icon_class = models.CharField(max_length=80, default="fas fa-building")
    image = models.ImageField(upload_to='industries/', null=True, blank=True)
    description = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='products/', null=True, blank=True)
    link = models.URLField(blank=True)
    icon_class = models.CharField(max_length=80, default="fas fa-box")
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

class ResearchItem(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True, help_text="Short description for the card")
    content = RichTextUploadingField(blank=True, null=True, verbose_name="Detailed Research")
    image = models.ImageField(upload_to='research/', null=True, blank=True)
    link = models.URLField(blank=True, help_text="Optional external link (e.g. ArXiv)")
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            original_slug = slugify(self.title)
            queryset = ResearchItem.objects.all().filter(slug__iexact=original_slug).count()
            
            count = 1
            slug = original_slug
            while(queryset):
                slug = original_slug + '-' + str(count)
                count += 1
                queryset = ResearchItem.objects.all().filter(slug__iexact=slug).count()
            
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self): return self.title

class JobOpening(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = RichTextUploadingField()
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
