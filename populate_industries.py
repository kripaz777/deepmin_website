import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from core.models import Industry

# Clear existing industries
print("Clearing existing industries...")
Industry.objects.all().delete()

industries_data = [
    {
        "name": "Healthcare & Biotech",
        "icon_class": "fas fa-dna",
        "description": "Accelerating drug discovery and enabling precision medicine through generative protein design and patient data analysis.",
        "featured": True
    },
    {
        "name": "Fintech & Banking",
        "icon_class": "fas fa-coins",
        "description": "Real-time fraud detection, algorithmic high-frequency trading, and automated regulatory compliance agents.",
        "featured": True
    },
    {
        "name": "Smart Manufacturing",
        "icon_class": "fas fa-industry",
        "description": "Predictive maintenance digital twins and autonomous supply chain optimization agents.",
        "featured": True
    },
    {
        "name": "Retail & E-Commerce",
        "icon_class": "fas fa-shopping-bag",
        "description": "Hyper-personalized recommendation engines and autonomous customer support representatives.",
        "featured": True
    },
     {
        "name": "Energy & Utilities",
        "icon_class": "fas fa-bolt",
        "description": "Grid load forecasting, renewable energy distribution optimization, and infrastructure monitoring.",
        "featured": True
    },
    {
        "name": "Legal & Compliance",
        "icon_class": "fas fa-balance-scale",
        "description": "Automated contract review, case precedent analysis, and regulatory risk assessment.",
        "featured": True
    }
]

print("Creating new industries...")
for item in industries_data:
    Industry.objects.create(**item)
    print(f"Created: {item['name']}")

print("Done! Industries populated.")
