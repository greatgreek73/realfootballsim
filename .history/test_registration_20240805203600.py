import os
import django
import random

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project_name.settings")
django.setup()

from django.db import transaction
from clubs.models import Club
from competitions.models import Country
from competitions.utils import add_club_to_championship

def generate_club_name():
    prefixes = ["FC", "United", "City", "Sporting", "Athletic"]
    suffixes = ["Lions", "Eagles", "Tigers", "Hawks", "Bears"]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"

@transaction.atomic
def register_clubs(country_code, num_clubs):
    country = Country.objects.get(code=country_code)
    for i in range(num_clubs):
        club_name = f"{generate_club_name()} {i+1}"
        club = Club.objects.create(name=club_name, country=country.code)
        championship = add_club_to_championship(club)
        print(f"Registered {club.name} in {championship.league.name}")

if __name__ == "__main__":
    register_clubs("GR", 19)  # Регистрируем 19 клубов в Греции