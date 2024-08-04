from django.core.management.base import BaseCommand
from competitions.models import Country, League
from django_countries import countries

class Command(BaseCommand):
    help = 'Setup initial countries and leagues'

    def handle(self, *args, **kwargs):
        # Создаем страны
        for code, name in list(countries)[:10]:  # Для примера создадим только 10 стран
            country, created = Country.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created country {name}'))

            # Создаем высшую лигу для каждой страны
            league, created = League.objects.get_or_create(
                name=f"{name} Premier League",
                country=country,
                level=1
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created league {league.name}'))

        self.stdout.write(self.style.SUCCESS('Initial setup completed'))