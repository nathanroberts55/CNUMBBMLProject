from typing import Union
from db.models import *
from db.database import engine, create_db_and_tables
from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
@app.get("/")
def root():
    return {
        "Version": "0.0.1",
        "Author":"@naterobertstech",
        "LastUpdated": "2023-02-16"
        }

# -- Players Endpoint ---

@app.get("/players/")
def read_players():
    with Session(engine) as session:
        players = session.exec(select(Player)).all()
        return players
    
@app.get("/players/{player_id}", response_model=PlayerReadWithTeam)
def read_player(player_id: UUID):
    with Session(engine) as session:
        player = session.get(Player, player_id)
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    
@app.post('/players/', response_model=PlayerRead)
def create_player(player: PlayerCreate):
    with Session(engine) as session:
        db_player = Player.from_orm(player)
        session.add(db_player)
        session.commit()
        session.refresh(db_player)
        return db_player

# -- Teams Endpoint ---
@app.get("/teams/")
def read_team():
    with Session(engine) as session:
        teams = session.exec(select(Team)).all()
        return teams

@app.get("/teams/{team_id}", response_model=TeamReadWithPlayers)
def read_team(team_id: UUID):
    with Session(engine) as session:
        team = session.get(Team, team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

@app.post('/teams/', response_model=TeamRead)
def create_team(team: TeamCreate):
    with Session(engine) as session:
        db_team = Team.from_orm(team)
        session.add(db_team)
        session.commit()
        session.refresh(db_team)
        return db_team

# -- Games Endpoint ---
@app.get("/games/")
def read_games():
    with Session(engine) as session:
        teams = session.exec(select(Game)).all()
        return teams

@app.get("/games/{game_id}", response_model=GamesReadWithTeams)
def read_game(game_id: UUID):
    with Session(engine) as session:
        game = session.get(Game, game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

@app.post('/games/', response_model=GameRead)
def create_game(game: GameCreate):
    with Session(engine) as session:
        db_game = Game.from_orm(game)
        session.add(db_game)
        session.commit()
        session.refresh(db_game)
        return db_game

# -- Seasons Endpoint ---
@app.get("/seasons/")
def read_seasons():
    with Session(engine) as session:
        seasons = session.exec(select(Season)).all()
        return seasons

@app.get("/seasons/{season_id}", response_model=SeasonReadWithGames)
def read_season(season_id: UUID):
    with Session(engine) as session:
        season = session.get(Season, season_id)
        if not season:
            raise HTTPException(status_code=404, detail="Season not found")
        return season

@app.post('/seasons/', response_model=SeasonRead)
def create_season(season: SeasonCreate):
    with Session(engine) as session:
        db_season = Season.from_orm(season)
        session.add(db_season)
        session.commit()
        session.refresh(db_season)
        return db_season

# -- Stat Lines Endpoint ---
@app.get("/statline/")
def read_statline():
    with Session(engine) as session:
        teams = session.exec(select(StatLine)).all()
        return teams

@app.post('/statline/', response_model=StatLineRead)
def create_statline(statline: StatLineCreate):
    with Session(engine) as session:
        db_statline = StatLine.from_orm(statline)
        session.add(db_statline)
        session.commit()
        session.refresh(db_statline)
        return db_statline