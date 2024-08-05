from django.contrib import admin
from .models import League, Championship, Season, Country, ChampionshipParticipation

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'level')
    list_filter = ('country', 'level')
    search_fields = ('name', 'country__name')

class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ('league', 'season', 'get_country')
    list_filter = ('league', 'season')
    search_fields = ('league__name', 'season__number')

    def get_country(self, obj):
        return obj.league.country
    get_country.short_description = 'Country'
    get_country.admin_order_field = 'league__country'

class SeasonAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('number',)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class ChampionshipParticipationAdmin(admin.ModelAdmin):
    list_display = ('championship', 'club', 'points', 'games_played')
    list_filter = ('championship', 'club')
    search_fields = ('championship__league__name', 'club__name')

admin.site.register(League, LeagueAdmin)
admin.site.register(Championship, ChampionshipAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ChampionshipParticipation, ChampionshipParticipationAdmin)