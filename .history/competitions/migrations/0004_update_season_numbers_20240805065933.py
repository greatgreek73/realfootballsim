from django.db import migrations

def update_season_numbers(apps, schema_editor):
    Season = apps.get_model('competitions', 'Season')
    seasons = Season.objects.all().order_by('start_date')
    for index, season in enumerate(seasons, start=1):
        season.number = index
        season.save()

class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '####_previous_migration'),  # Замените #### на номер предыдущей миграции
    ]

    operations = [
        migrations.RunPython(update_season_numbers),
    ]