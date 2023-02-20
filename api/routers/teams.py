from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from db.team_model import *
from dependencies import Session, get_session

router = APIRouter(
    prefix="/teams",
    tags=["seasons"]
)

# === Teams Endpoint ===
@router.get("/")
def read_team(*, session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams

@router.get("/{team_id}", response_model=TeamReadWithPlayers)
def read_team(*, session: Session = Depends(get_session), team_id: UUID):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post('/', response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@router.patch("/{team_id}", response_model=TeamRead)
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