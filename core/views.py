from django.shortcuts import render, get_object_or_404, redirect
from .models import SiteSettings, Service, Project, Training, BlogPost, TeamMember, Testimonial, Industry, Product, ResearchItem, JobOpening
from .forms import ContactForm, ApplicationForm
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

def get_site_settings():
    return SiteSettings.objects.first()

def index(request):
    settings_obj = get_site_settings()
    services = Service.objects.all().order_by('order')[:6]
    projects = Project.objects.filter(featured=True).order_by('-created_at')[:6]
    trainings = Training.objects.filter(active=True)[:3]
    testimonials = Testimonial.objects.all()[:6]
    industries = Industry.objects.all()[:4]
    context = {
        'site_settings': settings_obj,
        'services': services,
        'projects': projects,
        'trainings': trainings,
        'testimonials': testimonials,
        'industries': industries
    }
    return render(request, 'core/index.html', context)

def services_view(request):
    settings_obj = get_site_settings()
    services = Service.objects.all().order_by('order')
    return render(request, 'core/services.html', {'services': services, 'site_settings': settings_obj})

def projects_view(request):
    settings_obj = get_site_settings()
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'core/projects.html', {'projects': projects,'site_settings': settings_obj})

def trainings_view(request):
    settings_obj = get_site_settings()
    trainings = Training.objects.filter(active=True)
    return render(request, 'core/trainings.html', {'trainings': trainings,'site_settings': settings_obj})

def about_view(request):
    settings_obj = get_site_settings()
    team = TeamMember.objects.all()
    return render(request, 'core/about.html', {'team': team,'site_settings': settings_obj})

def blog_list(request):
    settings_obj = get_site_settings()
    posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    return render(request, 'core/blog_list.html', {'posts': posts,'site_settings': settings_obj})

def blog_detail(request, slug):
    settings_obj = get_site_settings()
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, 'core/blog_detail.html', {'post': post,'site_settings': settings_obj})

def contact_view(request):
    settings_obj = get_site_settings()
    sent = request.GET.get('sent')
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            if settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
                try:
                    send_mail(
                        f"Contact: {msg.subject or 'New message'}",
                        msg.message,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL],
                    )
                except Exception:
                    pass
            return redirect(reverse('core:contact') + '?sent=1')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form, 'sent': sent,'site_settings': settings_obj})

def careers_view(request):
    settings_obj = get_site_settings()
    jobs = JobOpening.objects.filter(active=True).order_by('-posted_at')
    applied = request.GET.get('applied')
    form = ApplicationForm()
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save()
            if settings.EMAIL_BACKEND != 'django.core.mail.backends.console.EmailBackend':
                try:
                    send_mail(
                        f"New application: {app.name}",
                        app.cover_message or 'Application received',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.DEFAULT_FROM_EMAIL],
                    )
                except Exception:
                    pass
            return redirect(reverse('core:careers') + '?applied=1')
    return render(request, 'core/careers.html', {'site_settings': settings_obj,'jobs': jobs, 'form': form, 'applied': applied})

def products_view(request):
    settings_obj = get_site_settings()
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products,'site_settings': settings_obj})

def research_view(request):
    settings_obj = get_site_settings()
    items = ResearchItem.objects.all()
    return render(request, 'core/research.html', {'items': items,'site_settings': settings_obj})
