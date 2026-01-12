import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from core.models import Product

# Clear existing products
print("Clearing existing products...")
Product.objects.all().delete()

products_data = [
    {
        "name": "NeuroCore Agentic Framework",
        "description": "The enterprise-grade orchestration engine for building, deploying, and managing autonomous AI agents at scale.",
        "icon_class": "fas fa-network-wired",
        "featured": True
    },
    {
        "name": "Nexus Knowledge Gateway",
        "description": "A centralized RAG (Retrieval-Augmented Generation) pipeline that connects your private data silos to advanced LLMs securely.",
        "icon_class": "fas fa-database",
        "featured": True
    },
    {
        "name": "Sentinel Guard",
        "description": "Real-time AI monitoring and defense system that detects adversarial attacks and ensures model compliance.",
        "icon_class": "fas fa-shield-alt",
        "featured": True
    }
]

print("Creating new products...")
for item in products_data:
    # Use placeholder images or leave blank for now, icon will be used
    Product.objects.create(**item)
    print(f"Created: {item['name']}")

print("Done! Products populated.")
