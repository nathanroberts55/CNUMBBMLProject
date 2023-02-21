from typing import List, Optional, TYPE_CHECKING
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .team_model import Team
    from .season_model import Season
    from .game_model import Game, GameRead
    from .player_model import Player, PlayerRead
    
# === Stat Line Models ===
class StatLineBase(SQLModel):
    date: datetime.date
    fgm: int = Field(default=0)
    fga: int = Field(default=0)
    fg_pct: float = Field(default=0.0)
    three_fgm: int = Field(default=0)
    three_fga: int = Field(default=0)
    three_pt_pct: float = Field(default=0.0)
    ftm: int = Field(default=0)
    fta: int = Field(default=0)
    ft_pct: float = Field(default=0.0)
    off_reb: int = Field(default=0)
    def_reb: int = Field(default=0)
    tot_reb: int = Field(default=0)
    pf: int = Field(default=0)
    ast: int = Field(default=0)
    to: int = Field(default=0)
    blk: int = Field(default=0)
    stl: int = Field(default=0)
    pts: int = Field(default=0)
    
class StatLine(StatLineBase, table=True):
    __tablename__ = "statLines"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    player_id: Optional[UUID] = Field(default=None, foreign_key="players.id")
    game_id: Optional[UUID] = Field(default=None, foreign_key="games.id")
    season_id: Optional[UUID] = Field(default=None, foreign_key="seasons.id")
    team_id: Optional[UUID] = Field(default=None, foreign_key="teams.id")
    
class StatLineCreate(StatLineBase):
    pass
    
class StatLineRead(StatLineBase):
    id: UUID
    
class StatLineUpdate(SQLModel):
    date: Optional[datetime.date] = None
    fgm: Optional[int] = None
    fga: Optional[int] = None
    fg_pct: Optional[float] = None
    three_fgm: Optional[int] = None
    three_fga: Optional[int] = None
    three_pt_pct: Optional[float] = None
    ftm: Optional[int] = None
    fta: Optional[int] = None
    ft_pct: Optional[float] = None
    off_reb: Optional[int] = None
    def_reb: Optional[int] = None
    tot_reb: Optional[int] = None
    pf: Optional[int] = None
    ast: Optional[int] = None
    to: Optional[int] = None
    blk: Optional[int] = None
    stl: Optional[int] = None
    pts: Optional[int] = None 
    
# === Relational Model Views ===

class StatLineReadWithPlayerAndTeam(StatLineRead):
    game_id: Optional["GameRead"] = None
    player_id: Optional["PlayerRead"] = None