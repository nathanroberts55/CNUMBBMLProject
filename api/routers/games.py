from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlmodel import Session, select
from db.models import *

router = APIRouter(
    prefix="/games",
    tags=["games"],
)

# === Games Endpoint ===
@router.get("/")
def read_games(*, session: Session = Depends(get_session)):
    teams = session.exec(select(Game)).all()
    return teams

@router.get("/{game_id}", response_model=GamesReadWithTeams)
def read_game(*, session: Session = Depends(get_session), game_id: UUID):
    game = session.get(Game, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post('/', response_model=GameRead)
def create_game(*, session: Session = Depends(get_session), game: GameCreate):
    
    query_team_1 = select(Team.id).where(Team.name == game.team_1)
    query_team_2 = select(Team.id).where(Team.name == game.team_2)
    
    team_1 = session.exec(query_team_1).first()
    team_2 = session.exec(query_team_2).first()
    
    if not team_1 and not team_2:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db_game = Game.from_orm(game)
    db_game. team1_id = team_1
    db_game. team2_id = team_2
    session.add(db_game)
    session.commit()
    session.refresh(db_game)
    return db_game

@router.patch("/{game_id}", response_model=GameRead)
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

# === Stat Endpoints ===
""" 
Want to follow the syntax of /{entity}/{entity.id}/stats
That way we can get the data of an individual player, team, game, season but for the entity
For example /players/2/stats will return all the statlines for the player with the matching ID
Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
preprocessing or query strings in the URL.
"""

@router.get("/{game_id}/stats", response_model=GameWithStatLines)
def get_games_stats(*, session: Session = Depends(get_session), game_id: UUID):
    pass