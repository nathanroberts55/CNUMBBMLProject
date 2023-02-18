from typing import List, Optional
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

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

# === Models ===
        
# === Player Models ===
class TeamBase(SQLModel):
    name: str

    
class Team(TeamBase, table=True):
    __tablename__ = "teams"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    players: Optional[List["Player"]] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: UUID

class TeamUpdate(SQLModel):
    name: Optional[str] = None

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
    team: Optional[Team] = Relationship(back_populates='players')

class PlayerCreate(PlayerBase):
    team_name:str       

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

# === Season Models ===
class SeasonBase(SQLModel):
    start_year: int
    end_year: int
    
class Season(SeasonBase, table=True):
    __tablename__ = "seasons"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships.
    games: Optional[List["Game"]] = Relationship(back_populates="season")
    
class SeasonCreate(SeasonBase):
    pass

class SeasonRead(SeasonBase):
    id: UUID

class SeasonUpdate(SQLModel):
    start_year: Optional[int] = None
    end_year: Optional[int] = None

# === Game Models ===   
class GameBase(SQLModel):
    date: datetime.date
    
class Game(GameBase, table=True):
    __tablename__ = "games"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    season_id: Optional[UUID] = Field(default=None, foreign_key="seasons.id")
    season: Optional[Season] = Relationship(back_populates='games')
    teams_id: Optional[List[UUID]] = Field(default=None, foreign_key="teams.id")

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: UUID

class GameUpdate(SQLModel):
    date: Optional[datetime.date] = None
    
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

class PlayerReadWithTeam(PlayerRead):
    team: Optional[TeamRead] = None
    
class TeamReadWithPlayers(TeamRead):
    players: Optional[List[PlayerRead]] = []

class GamesReadWithTeams(GameRead):
    teams_id: Optional[List[TeamRead]] = []

class SeasonReadWithGames(SeasonRead):
    games: Optional[List[GameRead]] = []

class StatLineReadWithPlayerAndTeam(StatLineRead):
    game_id: Optional[GameRead] = None
    player_id: Optional[PlayerRead] = None