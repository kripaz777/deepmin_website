from django.contrib import admin
from .models import SiteSettings, Service, Project, Training, BlogPost, TeamMember, Testimonial, Industry, Product, ResearchItem, JobOpening, Application, ContactMessage, CoreValue

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)
    fieldsets = (
        ('General', {
            'fields': ('site_name', 'logo', 'copyright_text')
        }),
        ('Hero Section', {
            'fields': ('hero_video', 'hero_phrases', 'hero_title', 'hero_subtitle')
        }),
        ('What We Do Section', {
            'fields': ('what_we_do_subtitle', 'what_we_do_title', 'what_we_do_desc')
        }),
        ('Footer Section', {
            'fields': ('footer_text', 'facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url', 'youtube_url', 'github_url')
        }),
        ('Contact Info', {
            'fields': ('contact_email', 'contact_phone', 'contact_address')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)

@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','category','featured','created_at')
    list_filter = ('featured','category')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'level', 'students_count', 'is_popular', 'active')
    list_filter = ('active', 'is_popular', 'level', 'mode')
    search_fields = ('title', 'summary')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','category','published','created_at')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name','role')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author','company')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'featured')
    list_editable = ('featured',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class', 'featured')
    list_editable = ('featured',)

@admin.register(ResearchItem)
class ResearchItemAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ('title','location','remote','active','posted_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name','email','job','created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject','created_at')
