from django.views.generic import ListView, DetailView
from .models import Championship, ChampionshipParticipation

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