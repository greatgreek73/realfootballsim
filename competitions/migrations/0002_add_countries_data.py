from django.db import migrations
from django_countries import countries

def add_countries(apps, schema_editor):
    Country = apps.get_model('competitions', 'Country')
    for code, name in list(countries):
        Country.objects.get_or_create(code=code, defaults={'name': name})

def remove_countries(apps, schema_editor):
    Country = apps.get_model('competitions', 'Country')
    Country.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_countries, remove_countries),
    ]