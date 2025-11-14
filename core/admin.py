from django.contrib import admin
from .models import SiteSettings, Service, Project, Training, BlogPost, TeamMember, Testimonial, Industry, Product, ResearchItem, JobOpening, Application, ContactMessage

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','category','featured','created_at')
    list_filter = ('featured','category')

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title','duration','mode','active')

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
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

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
