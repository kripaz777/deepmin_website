import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deepminds.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='tester').exists():
        User.objects.create_superuser('tester', 'tester@example.com', 'password123')
        print("Superuser 'tester' created.")
    else:
        print("Superuser 'tester' already exists.")
except Exception as e:
    print(f"Error: {e}")
