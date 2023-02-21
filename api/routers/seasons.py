from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlmodel import Session, select
from db.models import *

router = APIRouter(
    prefix="/seasons",
    tags=["seasons"],
)


# === Seasons Endpoint ===
@router.get("/")
def read_seasons(*, session: Session = Depends(get_session)):
    seasons = session.exec(select(Season)).all()
    return seasons

@router.get("/{season_id}", response_model=SeasonRead)
def read_season(*, session: Session = Depends(get_session), season_id: UUID):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season

@router.post('/', response_model=SeasonRead)
def create_season(*, session: Session = Depends(get_session), season: SeasonCreate):
    db_season = Season.from_orm(season)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season

@router.patch("/{season_id}", response_model=SeasonRead)
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

# === Stat Endpoints ===
""" 
Want to follow the syntax of /{entity}/{entity.id}/stats
That way we can get the data of an individual player, team, game, season but for the entity
For example /players/2/stats will return all the statlines for the player with the matching ID
Can let the front end handle the aggregation and math. That should hopefully reduce the need for any 
preprocessing or query strings in the URL.
"""

@router.get("/{season_id}/stats", response_model=SeasonWithStatLines)
def get_seasons_stats(*, session: Session = Depends(get_session), season_id: UUID):
    pass