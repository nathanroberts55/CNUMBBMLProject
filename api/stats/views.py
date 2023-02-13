from django.shortcuts import render
from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,UpdateModelMixin,RetrieveModelMixin,CreateModelMixin

# Create your views here.
class StatLineViewSet(
        CreateModelMixin,
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or retrieving items.
    """
    queryset = Stat_Line.objects.all()
    serializer_class = StatLineSerializer
    
class GameViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin, 
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or retrieving items.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
class PlayerViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin, 
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or retrieving items.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    
class TeamViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin, 
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or retrieving Teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
class SeasonViewSet(
        ListModelMixin,
        RetrieveModelMixin,
        CreateModelMixin, 
        viewsets.GenericViewSet
        ):
    """
    A simple ViewSet for listing or retrieving Seasons.
    """
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    