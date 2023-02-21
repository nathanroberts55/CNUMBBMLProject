from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .statline_model import StatLine, StatLineRead
    from .player_model import Player, PlayerRead
    
# === Team Models ===
class TeamBase(SQLModel):
    name: str = Field(default=None, unique=True)

    
class Team(TeamBase, table=True):
    __tablename__ = "teams"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    players: Optional[List["Player"]] = Relationship(back_populates="team")
    stats: Optional[List["StatLine"]] = Relationship()

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: UUID

class TeamUpdate(SQLModel):
    name: Optional[str] = None
    
# === Relational Model Views ===

class TeamReadWithPlayers(TeamRead):
    players: Optional[List["PlayerRead"]] = []
    
class TeamWithStatLines(TeamRead):
    stats: Optional[List["StatLineRead"]] = []