from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db.game_model import *
from dependencies import Session, get_session

router = APIRouter(
    prefix="/games",
    tags=["games"]
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
    db_game = Game.from_orm(game)
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