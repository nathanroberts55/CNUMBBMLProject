from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db.season_model import *
from dependencies import Session, get_session

router = APIRouter(
    prefix="/seasons",
    tags=["seasons"]
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