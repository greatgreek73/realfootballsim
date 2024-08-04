from django.db import transaction
from django.utils import timezone
from .models import League, Championship, ChampionshipParticipation, Season
from clubs.models import Club
import random

def create_or_get_current_season():
    current_year = timezone.now().year
    season, created = Season.objects.get_or_create(
        year=current_year,
        defaults={
            'start_date': f'{current_year}-08-01',
            'end_date': f'{current_year+1}-05-31'
        }
    )
    return season

@transaction.atomic
def create_championships_for_season(season):
    leagues = League.objects.all()
    for league in leagues:
        Championship.objects.get_or_create(league=league, season=season)

def generate_team_name(country_name):
    prefixes = ["FC", "United", "City", "Sporting", "Athletic"]
    suffixes = ["Lions", "Eagles", "Tigers", "Hawks", "Bears"]
    return f"{random.choice(prefixes)} {country_name} {random.choice(suffixes)}"

@transaction.atomic
def fill_championship_with_computer_teams(championship):
    current_teams = ChampionshipParticipation.objects.filter(championship=championship).count()
    teams_needed = championship.league.max_teams - current_teams

    if teams_needed > 0:
        for i in range(teams_needed):
            team_name = generate_team_name(championship.league.country.name)
            computer_club = Club.objects.create(
                name=team_name,
                country=championship.league.country.code,
                is_computer_managed=True,
                current_league=championship.league,
                current_championship=championship
            )
            ChampionshipParticipation.objects.create(championship=championship, club=computer_club)

@transaction.atomic
def add_club_to_championship(club):
    country = club.country
    lowest_league = League.objects.filter(country=country).order_by('-level').first()
    
    print(f"Adding club {club.name} to championship. Country: {country}, Lowest league: {lowest_league}")
    
    if not lowest_league:
        print(f"No league found for country {country}. Creating a new one.")
        lowest_league = League.objects.create(name=f"{country.name} League", country=country, level=1)
    
    current_season = create_or_get_current_season()
    championship, created = Championship.objects.get_or_create(league=lowest_league, season=current_season)
    
    print(f"Championship: {championship}, Created: {created}")
    
    participations = ChampionshipParticipation.objects.filter(championship=championship)
    if participations.count() < lowest_league.max_teams:
        ChampionshipParticipation.objects.create(championship=championship, club=club)
        print(f"Added {club.name} to {championship}")
    else:
        # Заменяем компьютерную команду на новую
        computer_team = participations.filter(club__is_computer_managed=True).first()
        if computer_team:
            computer_team.club.delete()
            ChampionshipParticipation.objects.create(championship=championship, club=club)
            print(f"Replaced computer team with {club.name} in {championship}")
        else:
            # Если нет компьютерных команд, создаем новую лигу
            new_league = League.objects.create(
                name=f"{country.name} League {lowest_league.level + 1}",
                country=country,
                level=lowest_league.level + 1
            )
            new_championship = Championship.objects.create(league=new_league, season=current_season)
            ChampionshipParticipation.objects.create(championship=new_championship, club=club)
            championship = new_championship
            print(f"Created new league and championship for {club.name}: {championship}")
    
    club.current_league = championship.league
    club.current_championship = championship
    club.save()
    
    print(f"Final club state: League: {club.current_league}, Championship: {club.current_championship}")
    
    return championship

@transaction.atomic
def end_season_and_promote_relegate():
    current_season = create_or_get_current_season()
    championships = Championship.objects.filter(season=current_season)

    for championship in championships:
        league = championship.league
        if league.level > 1:
            # Повышение команд
            top_teams = ChampionshipParticipation.objects.filter(championship=championship).order_by('-points')[:2]
            higher_league = League.objects.get(country=league.country, level=league.level-1)
            higher_championship = Championship.objects.get(league=higher_league, season=current_season)
            
            for team in top_teams:
                team.club.current_league = higher_league
                team.club.current_championship = higher_championship
                team.club.save()
                ChampionshipParticipation.objects.create(championship=higher_championship, club=team.club)
            
            # Понижение команд
            bottom_teams = ChampionshipParticipation.objects.filter(championship=higher_championship).order_by('points')[:2]
            for team in bottom_teams:
                team.club.current_league = league
                team.club.current_championship = championship
                team.club.save()
                ChampionshipParticipation.objects.create(championship=championship, club=team.club)

    # Создаем новый сезон и чемпионаты для него
    new_season = Season.objects.create(
        year=current_season.year + 1,
        start_date=f'{current_season.year + 1}-08-01',
        end_date=f'{current_season.year + 2}-05-31'
    )
    create_championships_for_season(new_season)

    # Переносим все клубы в новые чемпионаты
    clubs = Club.objects.all()
    for club in clubs:
        new_championship = Championship.objects.get(league=club.current_league, season=new_season)
        club.current_championship = new_championship
        club.save()
        ChampionshipParticipation.objects.create(championship=new_championship, club=club)