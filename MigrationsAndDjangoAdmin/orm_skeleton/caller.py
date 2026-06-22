import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
from main_app.models import UniqueBrands
UniqueBrands.objects.all().d