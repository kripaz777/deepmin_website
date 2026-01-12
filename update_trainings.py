import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from core.models import Training

def update_training_categories():
    trainings = Training.objects.all()
    categories = ['AI Engineering', 'Agentic Workflows', 'Data Science', 'Machine Learning']
    
    for i, t in enumerate(trainings):
        cat = categories[i % len(categories)]
        t.category = cat
        t.save()
        print(f"Updated training '{t.title}' with category '{cat}'.")

if __name__ == "__main__":
    update_training_categories()
