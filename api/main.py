from typing import Union
from db.models import *
from db.database import engine, create_db_and_tables
from sqlmodel import Session, select
from fastapi import FastAPI, HTTPException, Depends

def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

# === Startup Function ===
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
# === API Information ===
@app.get("/")
def root():
    return {
        "Version": "0.0.1",
        "Author":"@naterobertstech",
        "LastUpdated": "2023-02-16"
        }

# === Players Endpoint ===

@app.get("/players/")
def read_players(*, session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players
    
@app.get("/players/{player_id}", response_model=PlayerReadWithTeam)
def read_player(*, session: Session = Depends(get_session), player_id: UUID):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
    
@app.post('/players/', response_model=PlayerRead)
def create_player(*, session: Session = Depends(get_session), player: PlayerCreate):
    statement = select(Team).where(Team.name == player.team_name)
    team = session.scalars(statement).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_player = Player.from_orm(player)
    db_player.team_id = team.id
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

@app.patch("/players/{player_id}", response_model=PlayerRead)
def update_player(*, session: Session = Depends(get_session),player_id: UUID, player: PlayerUpdate):
    db_player = session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_data = player.dict(exclude_unset=True)
    for key, value in player_data.items():
        setattr(db_player, key, value)
    db_player.last_modified = datetime.datetime.utcnow()
    session.add(db_player)
    session.commit()
    session.refresh(db_player)
    return db_player

# === Teams Endpoint ===
@app.get("/teams/")
def read_team(*, session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams

@app.get("/teams/{team_id}", response_model=TeamReadWithPlayers)
def read_team(*, session: Session = Depends(get_session), team_id: UUID):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@app.post('/teams/', response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(*, session: Session = Depends(get_session),team_id: UUID, team: TeamUpdate):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    db_team.last_modified = datetime.datetime.utcnow()
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# === Games Endpoint ===
@app.get("/games/")
def read_games(*, session: Session = Depends(get_session)):
    teams = session.exec(select(Game)).all()
    return teams

@app.get("/games/{game_id}", response_model=GamesReadWithTeams)
def read_game(*, session: Session = Depends(get_session), game_id: UUID):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.post('/games/', response_model=GameRead)
def create_game(*, session: Session = Depends(get_session), game: GameCreate):
    db_game = Game.from_orm(game)
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game

@app.patch("/games/{game_id}", response_model=GameRead)
def update_game(*, session: Session = Depends(get_session),game_id: UUID, game: GameUpdate):
    db_game = session.get(Game, game_id)
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    game_data = game.dict(exclude_unset=True)
    for key, value in game_data.items():
        setattr(db_game, key, value)
    db_game.last_modified = datetime.datetime.utcnow()
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game


# === Seasons Endpoint ===
@app.get("/seasons/")
def read_seasons(*, session: Session = Depends(get_session)):
    seasons = session.exec(select(Season)).all()
    return seasons

@app.get("/seasons/{season_id}", response_model=SeasonReadWithGames)
def read_season(*, session: Session = Depends(get_session), season_id: UUID):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season

@app.post('/seasons/', response_model=SeasonRead)
def create_season(*, session: Session = Depends(get_session), season: SeasonCreate):
    db_season = Season.from_orm(season)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season

@app.patch("/seasons/{season_id}", response_model=SeasonRead)
def update_season(*, session: Session = Depends(get_session),season_id: UUID, season: SeasonUpdate):
    db_season = session.get(season, season_id)
    if not db_season:
        raise HTTPException(status_code=404, detail="Season not found")
    season_data = season.dict(exclude_unset=True)
    for key, value in season_data.items():
        setattr(db_season, key, value)
    db_season.last_modified = datetime.datetime.utcnow()
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season

# === Stat Lines Endpoint ===
@app.get("/statlines/")
def read_statline(*, session: Session = Depends(get_session)):
    teams = session.exec(select(StatLine)).all()
    return teams

@app.post('/statlines/', response_model=StatLineRead)
def create_statline(*, session: Session = Depends(get_session), statline: StatLineCreate):
    db_statline = StatLine.from_orm(statline)
    session.add(db_statline)
    session.commit()
    session.refresh(db_statline)
    return db_statline

@app.patch("/statlines/{statline_id}", response_model=StatLineRead)
def update_statline(*, session: Session = Depends(get_session),statline_id: UUID, statline: StatLineUpdate):
    db_statline = session.get(StatLine, statline_id)
    if not db_statline:
        raise HTTPException(status_code=404, detail="statline not found")
    statline_data = statline.dict(exclude_unset=True)
    for key, value in statline_data.items():
        setattr(db_statline, key, value)
    db_statline.last_modified = datetime.datetime.utcnow()
    session.add(db_statline)
    session.commit()
    session.refresh(db_statline)
    return db_statline


# === Stat Endpoints ===
""" 
Want to follow the syntax of /{entity}/{entity.id}/stats
That way we can get the data of an individual player, team, game, season but for the entity
For example /players/2/stats will return all the statlines for the player with the matching ID
Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
preprocessing or query strings in the URL.
"""