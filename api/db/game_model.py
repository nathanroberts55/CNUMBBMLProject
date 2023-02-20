from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4
import datetime
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from .team_model import Team, TeamRead
    
# === Game Models ===   
class GameBase(SQLModel):
    date: datetime.date
    
class Game(GameBase, table=True):
    __tablename__ = "games"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    teams_id: Optional[List[UUID]] = Field(default=None, foreign_key="teams.id")
    team: Optional["Team"] = Relationship(back_populates='players')

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: UUID

class GameUpdate(SQLModel):
    date: Optional[datetime.date] = None
    
# === Relational Model Views ===
    
class GamesReadWithTeams(GameRead):
    teams_id: Optional[List["TeamRead"]] = []
