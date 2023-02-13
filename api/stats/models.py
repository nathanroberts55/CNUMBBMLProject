from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
)

# --- Player Table ---   
class Player(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    
    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Players'
        ordering = ["id"]
        
    #--- Foreign Keys ---
    # stat_line = models.ForeignKey(Stat_Line, on_delete=models.CASCADE)
    # team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    #--- Model Fields ---
    full_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    height = models.CharField(max_length=50)
    weight = models.CharField(max_length=50)
    hometown_hs = models.CharField(max_length=50)
    jersey_num = models.IntegerField()
    
    def __str__(self):
        return self.full_name

# --- Team Table ---
class Team(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    
    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        ordering = ["id"]
        
    #--- Foreign Keys ---
    players = models.ManyToManyField(Player)
    
    #--- Model Fields ---
    name = models.CharField(null=False, max_length=50)
    
    def __str__(self):
        return self.name
    
# --- Game Table ---
class Game(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    
    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ["id"]
    
    #--- Foreign Keys ---
    teams = models.ManyToManyField(Team)

    
    #--- Model Fields ---

    
    # def __str__(self):
    #     return f'{self.team_1} vs. {self.team_2}'    


# --- Season Table ---
class Season(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        
        ordering = ["id"]
    
    #--- Foreign Keys ---
    games = models.ManyToManyField(Game)
    
    #--- Model Fields ---
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.start_year}-{self.end_year}'
    
# --- Stat Line Table ---
class Stat_Line(
    TimeStampedModel,
    ActivatorModel ,
    Model):
    
    class Meta:
        verbose_name = 'Stat Line'
        verbose_name_plural = 'Stat Lines'
        ordering = ["id"]
    
    #--- Foreign Keys ---
    player = models.ForeignKey(Player, on_delete=models.CASCADE)  
    game = models.ForeignKey(Game, on_delete=models.CASCADE)  
  
    #--- Model Fields ---
    date = models.DateField()
    fgm = models.IntegerField()
    fga = models.IntegerField()
    fg_pct = models.DecimalField(max_digits=3, decimal_places=3)
    three_fgm = models.IntegerField()
    three_fga = models.IntegerField()
    three_pt_pct = models.DecimalField(max_digits=3, decimal_places=3)
    ftm = models.IntegerField()
    fta = models.IntegerField()
    ft_pct = models.DecimalField(max_digits=3, decimal_places=3)
    off_reb = models.IntegerField()
    def_reb = models.IntegerField()
    tot_reb = models.IntegerField()
    pf = models.IntegerField()
    ast = models.IntegerField()
    to = models.IntegerField()
    blk = models.IntegerField()
    stl = models.IntegerField()
    pts = models.IntegerField()   