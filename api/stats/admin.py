from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('start_year', 'end_year', 'id', )
@admin.register(models.Stat_Line)
class StatLineAdmin(admin.ModelAdmin):
    list_display = ('date', 'id', )
@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', )
@admin.register(models.Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'jersey_num', 'id',)
@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', )
    
