from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = CountryField(unique=True)

    def __str__(self):
        return self.name

class League(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)
    max_teams = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.name} ({self.country.name})"

class Season(models.Model):
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.year}-{self.year+1}"

class Championship(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.league.name} - {self.season}"

class ChampionshipParticipation(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    club = models.OneToOneField('clubs.Club', on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    class Meta:
        unique_together = ('championship', 'club')

    def __str__(self):
        return f"{self.club.name} in {self.championship}"