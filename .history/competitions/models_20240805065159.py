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
    number = models.PositiveIntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['-number']

    def __str__(self):
        return f"Season {self.number}"

    @classmethod
    def get_current_season(cls):
        return cls.objects.first()

    @classmethod
    def create_next_season(cls):
        current_season = cls.get_current_season()
        if current_season:
            new_number = current_season.number + 1
        else:
            new_number = 1
        
        # You may want to adjust the date logic based on your requirements
        from datetime import date, timedelta
        start_date = date.today()
        end_date = start_date + timedelta(days=365)
        
        return cls.objects.create(number=new_number, start_date=start_date, end_date=end_date)

class Championship(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.league.name} - Season {self.season.number}"

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