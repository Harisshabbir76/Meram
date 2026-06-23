import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meram_events.settings')
django.setup()

from main.models import PageContent

for pc in PageContent.objects.all():
    print(f"ID: {pc.id}")
    print(f"Page: {pc.page}")
    print(f"Key: {pc.element_key}")
    print(f"Content EN: {pc.content_en}")
    print(f"Content AR: {pc.content_ar}")
    print(f"Styles EN: {pc.styles_en}")
    print(f"Styles AR: {pc.styles_ar}")
    print("-" * 50)
