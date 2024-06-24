# Generated by Django 5.0.4 on 2024-06-24 13:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clubs.club')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_selections', to='matches.match')),
            ],
            options={
                'unique_together': {('match', 'club')},
            },
        ),
    ]
