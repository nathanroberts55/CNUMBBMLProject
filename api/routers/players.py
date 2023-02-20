from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db.player_model import *
from dependencies import Session, get_session

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

# === Players Endpoint ===
@router.get("/")
async def read_players(*, session: Session = Depends(get_session)):
    players = session.exec(select(Player)).all()
    return players
    
@router.get("/{player_id}", response_model=PlayerReadWithTeam)
async def read_player(*, session: Session = Depends(get_session), player_id: UUID):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player
    
@router.post('/', response_model=PlayerRead)
async def create_player(*, session: Session = Depends(get_session), player: PlayerCreate):
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
async def update_player(*, session: Session = Depends(get_session),player_id: UUID, player: PlayerUpdate):
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