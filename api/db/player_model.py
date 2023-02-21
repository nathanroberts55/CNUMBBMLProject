from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .team_model import Team, TeamRead
    from .statline_model import StatLine, StatLineRead

# === Choices as Enums ===
class ClassEnum(str, Enum):
    freshman = 'Fr.'
    sophomore = 'So.'
    junior = 'Jr.'
    senior = 'Sr.'
    graduate = 'Gr.'
    
class PositionEnum(str, Enum):
    point_guard = 'PG'
    shooting_guard = 'SG'
    small_forward = 'SF'
    power_forward = 'PF'
    center = 'C'
    
# === Player Models ===
class PlayerBase(SQLModel):
    full_name: str 
    class_name: ClassEnum 
    position: PositionEnum 
    height: str
    weight: str
    hometown_hs:str
    jersey_num: int
    
class Player(PlayerBase, table=True):
    __tablename__ = "players"
    
    id: Optional[UUID]  = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    team_id: Optional[UUID]  = Field(default=None, foreign_key="teams.id")
    team: Optional["Team"] = Relationship(back_populates='players')
    stats: Optional[List["StatLine"]] = Relationship()

class PlayerCreate(PlayerBase):
    team_name: str       

class PlayerRead(PlayerBase):
    id: UUID       
    
class PlayerUpdate(SQLModel):
    full_name: Optional[str] = None
    class_name: Optional[ClassEnum] = None
    position: Optional[PositionEnum] = None
    height: Optional[str] = None
    weight: Optional[str] = None
    hometown_hs:Optional[str] = None
    jersey_num: Optional[int] = None
    
# === Relational Model Views ===

class PlayerReadWithTeam(PlayerRead):
    team: Optional["TeamRead"] = None
    
class PlayerWithStatLines(PlayerRead):
    stats: Optional[List["StatLineRead"]] = []