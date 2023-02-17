from typing import List, Optional
from uuid import UUID, uuid4
import datetime
from enum import Enum, IntEnum
from sqlmodel import Field, Relationship, SQLModel

# -- Choices as Enums
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

# -- Models
        
class TeamBase(SQLModel):
    name: str

    
class Team(TeamBase, table=True):
    __tablename__ = "teams"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_by: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    players: Optional[List["Player"]] = Relationship(back_populates="team")
    # games: Optional[List["Game"]] = Relationship(back_populates="teams")

class TeamCreate(TeamBase):
    pass

class TeamRead(TeamBase):
    id: UUID

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
    created_by: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    team_id: Optional[UUID]  = Field(default_factory=uuid4, foreign_key="teams.id")
    team: Optional[Team] = Relationship(back_populates='players')

class PlayerCreate(PlayerBase):
    pass       

class PlayerRead(PlayerBase):
    id: UUID       
    
class SeasonBase(SQLModel):
    start_year: int
    end_year: int
    
class Season(SeasonBase, table=True):
    __tablename__ = "seasons"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_by: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships.
    games: Optional[List["Game"]] = Relationship(back_populates="season")
    
class SeasonCreate(SeasonBase):
    pass

class SeasonRead(SeasonBase):
    id: UUID
 
class GameBase(SQLModel):
    date: datetime.date
    
class Game(GameBase, table=True):
    __tablename__ = "games"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_by: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    season_id: Optional[UUID] = Field(default_factory=uuid4, foreign_key="seasons.id")
    season: Optional[Season] = Relationship(back_populates='games')
    teams_id: Optional[List[UUID]] = Field(default_factory=uuid4, foreign_key="teams.id")

class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: UUID

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
    created_by: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    # Relationships
    player_id: Optional[UUID] = Field(default_factory=uuid4, foreign_key="players.id")
    game_id: Optional[UUID] = Field(default_factory=uuid4, foreign_key="games.id")
    
class StatLineCreate(StatLineBase):
    pass
    
class StatLineRead(StatLineBase):
    id: UUID
    
# -- Relational Models

class PlayerReadWithTeam(PlayerRead):
    team: Optional[Team]
    
class TeamReadWithPlayers(TeamRead):
    players: Optional[List["Player"]]

class GamesReadWithTeams(GameRead):
    teams_id: Optional[List[UUID]]

class SeasonReadWithGames(SeasonRead):
    games: Optional[List["Game"]]

class StatLineReadWithPlayerAndTeam(StatLineRead):
    game_id: Optional[UUID]
    player_id: Optional[UUID]