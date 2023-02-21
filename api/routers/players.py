from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlmodel import Session, select
from db.models import *

router = APIRouter(
    prefix="/players",
    tags=["players"],
)

# === Players Endpoint ===

@router.get("/")
def read_players(*, session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players
    
@router.get("/{player_id}", response_model=PlayerReadWithTeam)
def read_player(*, session: Session = Depends(get_session), player_id: UUID):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
    
@router.post('/', response_model=PlayerRead)
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

@router.patch("/{player_id}", response_model=PlayerRead)
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

# === Stat Endpoints ===
""" 
Want to follow the syntax of /{entity}/{entity.id}/stats
That way we can get the data of an individual player, team, game, season but for the entity
For example /players/2/stats will return all the statlines for the player with the matching ID
Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
preprocessing or query strings in the URL.
"""

@router.get("/{player_id}/stats", response_model=PlayerWithStatLines)
def get_players_stats(*, session: Session = Depends(get_session), player_id: UUID):
    pass