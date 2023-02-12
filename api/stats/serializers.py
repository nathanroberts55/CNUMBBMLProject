from collections import OrderedDict
from .models import *
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = (
            'id',
            'full_name',
            'class_name',
            'height',
            'weight',
            'position',
            'jersey_num',
            'hometown_hs',
        )
    
class CoachSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coach
        fields = (
            'id',
            'name',
        )
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'players',
        )
class GameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Game
        fields = (
            'id',
            'teams'
        )
class SeasonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Season
        fields = (
            'start_year',
            'end_year',
            'games',
        )
class StatLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat_Line
        # fields = (
        #     'date',
        #     'team_1',
        #     'team_2',
        #     'season_year'
        # )
        exclude = ['id', 
                   'activate_date', 
                   'deactivate_date',
                   'status'
                   ]