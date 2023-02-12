from collections import OrderedDict
from .models import *
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

class StatLineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stat_Line
        fields = (
            'date',
            'team_1',
            'team_2',
            'season_year'
        )
class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = (
            'stat_line'
        )
class PlayerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Player
        fields = (
            'full_name',
            'class_name',
            'height',
            'weight',
            'position',
            'jersey_num',
            'hometown_hs',
        )
class TeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = (
            'name'
        )
class SeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Season
        fields = (
            'stat_line'
        )
class CoachSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coach
        fields = (
            'name',
            'team'
        )