from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Championship, ChampionshipParticipation, Season, League
from .utils import create_or_get_current_season, create_championships_for_season, fill_championship_with_computer_teams

class ChampionshipListView(ListView):
    model = Championship
    template_name = 'competitions/championship_list.html'
    context_object_name = 'championships'

class ChampionshipDetailView(DetailView):
    model = Championship
    template_name = 'competitions/championship_detail.html'
    context_object_name = 'championship'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['standings'] = ChampionshipParticipation.objects.filter(championship=self.object).order_by('-points', '-goals_for', 'goals_against')
        return context

@staff_member_required
def create_season_and_championships(request):
    if request.method == 'POST':
        season = create_or_get_current_season()
        leagues = League.objects.all()
        
        for league in leagues:
            championship, created = Championship.objects.get_or_create(
                league=league,
                season=season
            )
            if created:
                fill_championship_with_computer_teams(championship)
                messages.success(request, f"Created championship for {league.name} and filled with computer teams.")
            else:
                messages.info(request, f"Championship for {league.name} already exists.")
        
        return redirect('competitions:championship_list')
    
    return render(request, 'competitions/create_season.html')