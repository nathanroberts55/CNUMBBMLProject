from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from sqlmodel import Session, select
from db.models import *

router = APIRouter(
    prefix="/statlines",
    tags=["statlines"],
)

# === Stat Lines Endpoint ===
@router.get("/")
def read_statline(*, session: Session = Depends(get_session)):
    teams = session.exec(select(StatLine)).all()
    return teams

@router.post('/', response_model=StatLineRead)
def create_statline(*, session: Session = Depends(get_session), statline: StatLineCreate):
    db_statline = StatLine.from_orm(statline)
    session.add(db_statline)
    session.commit()
    session.refresh(db_statline)
    return db_statline

@router.patch("/{statline_id}", response_model=StatLineRead)
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