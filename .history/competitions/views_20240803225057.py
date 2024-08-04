from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect
from django.contrib import messages
from .models import Championship, ChampionshipParticipation
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
    season = create_or_get_current_season()
    create_championships_for_season(season)
    championships = Championship.objects.filter(season=season)
    
    for championship in championships:
        fill_championship_with_computer_teams(championship)
    
    messages.success(request, f"New season {season} created with championships and filled with computer teams.")
    return redirect('admin:index')