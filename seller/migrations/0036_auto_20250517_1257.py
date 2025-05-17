from django.db import migrations
from django.utils.text import slugify

def generate_slugs(apps, schema_editor):
    BusinessInformation = apps.get_model('seller', 'BusinessInformation')
    for obj in BusinessInformation.objects.all():
        if not obj.slug:
            obj.slug = slugify(f"{obj.name}-{obj.id}")
            obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0029_businessinformation_slug_businessinformation_uuid_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_slugs),
    ]
