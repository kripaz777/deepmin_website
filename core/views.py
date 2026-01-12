from django.shortcuts import render, get_object_or_404, redirect
from .models import SiteSettings, Service, Project, Training, BlogPost, TeamMember, Testimonial, Industry, Product, ResearchItem, JobOpening, NewsletterSubscription, CoreValue
from .forms import ContactForm, ApplicationForm
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse

def get_site_settings():
    return SiteSettings.objects.first()

def index(request):
    settings_obj = get_site_settings()
    services = Service.objects.all().order_by('order')[:6]
    projects = Project.objects.filter(featured=True).order_by('-created_at')[:6]
    trainings = Training.objects.filter(active=True)[:3]
    testimonials = Testimonial.objects.all()[:6]
    industries = Industry.objects.all()[:6]
    products = Product.objects.filter(featured=True)[:3]
    context = {
        'site_settings': settings_obj,
        'services': services,
        'projects': projects,
        'products': products,
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
    category = request.GET.get('category')
    
    if category and category != 'All':
        trainings = Training.objects.filter(active=True, category=category)
    else:
        trainings = Training.objects.filter(active=True)
    
    # Get unique categories for the tabs
    categories = Training.objects.filter(active=True).values_list('category', flat=True).distinct()
    
    context = {
        'trainings': trainings,
        'site_settings': settings_obj,
        'categories': categories,
        'selected_category': category or 'All'
    }
    return render(request, 'core/trainings.html', context)

def training_detail(request, pk):
    settings_obj = get_site_settings()
    training = get_object_or_404(Training, pk=pk, active=True)
    return render(request, 'core/training_detail.html', {'training': training, 'site_settings': settings_obj})

def about_view(request):
    settings_obj = get_site_settings()
    team = TeamMember.objects.all()
    values = CoreValue.objects.all().order_by('order')
    return render(request, 'core/about.html', {'team': team,'site_settings': settings_obj, 'values': values})

def blog_list(request):
    settings_obj = get_site_settings()
    query = request.GET.get('q')
    if query:
        posts = BlogPost.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query),
            published=True
        ).order_by('-created_at')
    else:
        posts = BlogPost.objects.filter(published=True).order_by('-created_at')
    
    return render(request, 'core/blog_list.html', {'posts': posts,'site_settings': settings_obj, 'query': query})

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscription.objects.get_or_create(email=email)
            if request.headers.get('HX-Request'):
                return render(request, 'core/partials/newsletter_success.html')
            return redirect(reverse('core:blog') + '?subscribed=1')
    return redirect('core:blog')

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
        initial_data = {}
        if request.GET.get('subject'):
            initial_data['subject'] = request.GET.get('subject')
        if request.GET.get('message'):
            initial_data['message'] = request.GET.get('message')
        elif request.GET.get('ref'):
            initial_data['message'] = f"Interested in {request.GET.get('ref')}. I would like to book a demo."
            
        form = ContactForm(initial=initial_data)
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

def job_detail_view(request, pk):
    settings_obj = get_site_settings()
    job = get_object_or_404(JobOpening, pk=pk, active=True)
    form = ApplicationForm(initial={'job': job})
    
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
            return redirect(reverse('core:job_detail', kwargs={'pk': pk}) + '?applied=1')

    return render(request, 'core/job_detail.html', {'job': job, 'site_settings': settings_obj, 'form': form, 'applied': request.GET.get('applied')})

def products_view(request):
    settings_obj = get_site_settings()
    products = Product.objects.all()
    return render(request, 'core/products.html', {'products': products,'site_settings': settings_obj})

def research_view(request):
    settings_obj = get_site_settings()
    items = ResearchItem.objects.all()
    return render(request, 'core/research.html', {'items': items,'site_settings': settings_obj})

