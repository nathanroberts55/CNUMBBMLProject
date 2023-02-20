from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4
import datetime
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
    
# === Season Models ===
class SeasonBase(SQLModel):
    start_year: int
    end_year: int
    
class Season(SeasonBase, table=True):
    __tablename__ = "seasons"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_on: datetime.datetime = Field(default=datetime.datetime.utcnow())
    last_modified: datetime.datetime = Field(default=datetime.datetime.utcnow())
    
    
class SeasonCreate(SeasonBase):
    pass

class SeasonRead(SeasonBase):
    id: UUID

class SeasonUpdate(SQLModel):
    start_year: Optional[int] = None
    end_year: Optional[int] = None