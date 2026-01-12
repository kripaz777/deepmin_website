import os
import django
import random
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from core.models import Service, Project, Training, TeamMember, Testimonial, BlogPost
from django.utils.text import slugify
from django.utils import timezone

def populate():
    print("Populating database with dynamic data...")

    # 1. Services
    services_data = [
        {"title": "Agentic Workflow Automation", "short_description": "Architecting autonomous agents that handle complex business processes from end-to-end.", "icon_class": "fas fa-robot", "order": 1},
        {"title": "Data Science & Predictive Analytics", "short_description": "Transforming raw data into actionable insights using advanced statistical modeling and machine learning.", "icon_class": "fas fa-chart-line", "order": 2},
        {"title": "Enterprise LLM Solutions", "short_description": "Deploying custom, secure large language models tailored to your specific organizational data.", "icon_class": "fas fa-brain", "order": 3},
        {"title": "RAG & Knowledge Systems", "short_description": "Building Retrieval-Augmented Generation systems to turn your documents into actionable intelligence.", "icon_class": "fas fa-database", "order": 4},
        {"title": "AI & Data Strategy", "short_description": "Guiding organizations through the complexities of AI adoption, data governance, and digital transformation.", "icon_class": "fas fa-lightbulb", "order": 5},
    ]
    for s in services_data:
        Service.objects.get_or_create(title=s['title'], defaults=s)

    # 2. Trainings (Courses)
    trainings_data = [
        {
            "title": "Autonomous AI Agent Development",
            "summary": "Learn to build multi-agent systems using frameworks like LangChain, CrewAI, and AutoGen.",
            "price": 899.00,
            "discount_price": 599.00,
            "instructor_name": "Dr. Aayush Sharma",
            "rating": 5.0,
            "students_count": 450,
            "level": "Advanced",
            "duration": "10 Weeks",
            "mode": "Online Live",
            "is_popular": True
        },
        {
            "title": "Data Science Boot Camp 2026",
            "summary": "Master Python, SQL, and Machine Learning to become a high-impact data scientist in the AI era.",
            "price": 750.00,
            "discount_price": 499.00,
            "instructor_name": "Nitesh Yadav",
            "rating": 4.9,
            "students_count": 890,
            "level": "Intermediate",
            "duration": "12 Weeks",
            "mode": "Hybrid",
            "is_popular": True
        },
        {
            "title": "LLM Fine-tuning & Optimization",
            "summary": "Master the art of fine-tuning open-source models like Llama 3 and Mistral for specialized tasks.",
            "price": 650.00,
            "discount_price": 450.00,
            "instructor_name": "Rohan Gupta",
            "rating": 4.9,
            "students_count": 320,
            "level": "Expert",
            "duration": "8 Weeks",
            "mode": "Self-Paced",
            "is_popular": False
        },
    ]
    for t in trainings_data:
        Training.objects.get_or_create(title=t['title'], defaults=t)

    # 3. Testimonials
    testimonials_data = [
        {"quote": "DeepMinds deployed an agentic system that cut our operational costs by 60%. They are the leaders in AI.", "author": "Binod Chaudhary", "role": "CEO", "company": "CG Group"},
        {"quote": "Their data analysis and predictive modeling helped us forecast market trends with 95% accuracy.", "author": "Anjali Rai", "role": "CTO", "company": "Global Insight"},
        {"quote": "Their knowledge in RAG and Vector Databases helped us build a search engine 10x better than our old one.", "author": "Sandeep Lamichhane", "role": "Founder", "company": "DataFlow"},
    ]
    for test in testimonials_data:
        Testimonial.objects.get_or_create(author=test['author'], defaults=test)

    # 4. Projects
    projects_data = [
        {"title": "Autonomous Supply Chain Agent", "category": "Logistics AI", "short_description": "A multi-agent system that predicts and resolves supply chain disruptions in real-time.", "featured": True},
        {"title": "Consumer Behavior Analysis", "category": "Data Science", "short_description": "Large-scale data analysis project identifying emerging patterns in retail consumption.", "featured": True},
        {"title": "LegalDoc IntelliSearch", "category": "LegalTech", "short_description": "RAG-powered intelligence layer for searching across 100k+ legal documents.", "featured": True},
    ]
    for p in projects_data:
        Project.objects.get_or_create(title=p['title'], defaults=p)

    print("Success: AI & Data Science focused database populated!")

if __name__ == "__main__":
    populate()
