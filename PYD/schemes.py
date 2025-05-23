from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List, Optional
from datetime import date

class GenreCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class GenreReturn(BaseModel):
    id: int = Field(..., gt=0, example=1)
    name: str = Field(..., max_length=100)
    description: str = Field(None, max_length=500)

class MovieCreate(BaseModel):
    title: str = Field(..., max_length=100)
    year: int = Field(..., gt=1888, le=date.today().year)
    genres: List[int]=Field(None, example=[1,2])
    duration: int = Field(..., gt=0)
    rating: float = Field(None, ge=0, le=10)
    description: Optional[str] = None
    poster_url: Optional[str] = Field(None, min_length=2, max_length=200, example='example/example.png')
    
class MovieReturn(BaseModel):
    id: int = Field(..., gt=0, example=1)
    title: str = Field(..., max_length=100)
    year: int = Field(..., gt=1888, le=date.today().year)
    genres: List[GenreCreate]
    duration: int = Field(..., gt=0)
    rating: float = Field(None, ge=0, le=10)
    description: Optional[str] = None
    poster_url: Optional[str] = Field(..., min_length=2, max_length=200, example='example/example.png')

class MovieUpdate(BaseModel):
    title: Optional[str] = Field(..., max_length=100)
    year: Optional[int] = Field(..., gt=1888, le=date.today().year)
    genres: Optional[List[int]]=Field(None, example=[1,2])
    duration: Optional[int] = Field(..., gt=0)
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None
    poster_url: Optional[str] = Field(..., min_length=2, max_length=200, example='example/example.png')