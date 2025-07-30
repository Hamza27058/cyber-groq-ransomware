from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

# ------------- Tool Args -------------
class LimitArgs(BaseModel):
    limit: Optional[int] = Field(10, ge=1, le=1000)

class GroupArgs(BaseModel):
    group: str

class KeywordArgs(BaseModel):
    keyword: str
    limit: Optional[int] = Field(10, ge=1, le=1000)

class CountryArgs(BaseModel):
    countryCode: str = Field(..., min_length=2, max_length=2)

class DateArgs(BaseModel):
    year: int
    month: int = Field(..., ge=1, le=12)

class SectorArgs(BaseModel):
    sector: str
    countryCode: Optional[str] = Field(None, min_length=2, max_length=2)

# ------------- Unified response -------------
class ToolResponse(BaseModel):
    data: Dict[str, Any]

# ------------- Chat endpoints -------------
class AskRequest(BaseModel):
    query: str
    limit: int = Field(3, ge=1, le=10)  # keep small for free tier
    stream: bool = False

class AskResponse(BaseModel):
    answer: str
    model: str

