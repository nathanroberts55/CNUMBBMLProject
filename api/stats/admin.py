from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('id', 'stat_line')
@admin.register(models.Stat_Line)
class StatLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'team_1', 'team_2', 'season_year')
@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'stat_line')
@admin.register(models.Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team')
@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'position', 'jersey_num', 'stat_line')
@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'stat_line')
    
