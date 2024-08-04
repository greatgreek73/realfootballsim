from django.db import models
from django.conf import settings
from django_countries.fields import CountryField

class Club(models.Model):
    name = models.CharField(max_length=100, verbose_name="Club Name")
    country = CountryField(blank_label='(select country)', verbose_name="Country")
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Owner", related_name="club", null=True, blank=True)
    lineup = models.JSONField(null=True, blank=True)
    is_computer_managed = models.BooleanField(default=False, verbose_name="Computer Managed")
    current_league = models.ForeignKey('competitions.League', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Current League")
    current_championship = models.ForeignKey('competitions.Championship', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Current Championship")

    class Meta:
        verbose_name = "Club"
        verbose_name_plural = "Clubs"

    def __str__(self):
        return self.name

    def get_current_standing(self):
        if self.current_championship:
            return self.championshipparticipation_set.filter(championship=self.current_championship).first()
        return None

    def update_league(self, new_league):
        self.current_league = new_league
        self.save()

    def update_championship(self, new_championship):
        self.current_championship = new_championship
        self.save()

    @classmethod
    def replace_computer_team(cls, championship):
        computer_team = cls.objects.filter(
            current_championship=championship,
            is_computer_managed=True
        ).first()
        if computer_team:
            computer_team.delete()
            return True
        return False