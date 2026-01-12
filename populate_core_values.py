import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from core.models import CoreValue

def populate_values():
    values = [
        {
            'title': 'Innovation First',
            'description': 'Pushing the boundaries of what AI can achieve through continuous R&D and radical experimentation.',
            'icon_class': 'fas fa-microchip',
            'order': 1
        },
        {
            'title': 'Reliability',
            'description': 'Building trusted, ethical, and enterprise-grade systems that perform flawlessly in production.',
            'icon_class': 'fas fa-shield-alt',
            'order': 2
        },
        {
            'title': 'Community',
            'description': 'Democratizing AI knowledge through open-source contributions and our world-class academy.',
            'icon_class': 'fas fa-users',
            'order': 3
        }
    ]

    for val in values:
        obj, created = CoreValue.objects.get_or_create(
            title=val['title'],
            defaults={'description': val['description'], 'icon_class': val['icon_class'], 'order': val['order']}
        )
        if not created:
            obj.description = val['description']
            obj.icon_class = val['icon_class']
            obj.order = val['order']
            obj.save()
        print(f"Value '{val['title']}' {'created' if created else 'updated'}.")

if __name__ == "__main__":
    populate_values()
