from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .team_model import Team, TeamRead
    from .statline_model import StatLine, StatLineRead
    
# === Game Models ===   
class GameBase(SQLModel):
    date: datetime.date
    
class Game(GameBase, table=True):
    __tablename__ = "games"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    team1_id: Optional[UUID] = Field(default=None, foreign_key="teams.id")
    team2_id: Optional[UUID] = Field(default=None, foreign_key="teams.id")
    stats: Optional[List["StatLine"]] = Relationship()

class GameCreate(GameBase):
    team_1: str
    team_2: str

class GameRead(GameBase):
    id: UUID

class GameUpdate(SQLModel):
    date: Optional[datetime.date] = None
    
# === Relational Model Views ===
class GamesReadWithTeams(GameRead):
    team1_id: Optional["TeamRead"] = None
    team2_id: Optional["TeamRead"] = None
    
class GameWithStatLines(GameRead):
    stats: Optional[List["StatLineRead"]] = []