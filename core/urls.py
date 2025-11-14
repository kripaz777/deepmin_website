from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services_view, name='services'),
    path('products/', views.products_view, name='products'),
    path('projects/', views.projects_view, name='projects'),
    path('trainings/', views.trainings_view, name='trainings'),
    path('research/', views.research_view, name='research'),
    path('about/', views.about_view, name='about'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('careers/', views.careers_view, name='careers'),
]
