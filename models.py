from sqlalchemy import Column, Integer, String, ARRAY, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Genre(Base):  # 1
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    
class Movie(Base):  # N
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title= Column(String(100), nullable=False)
    year=Column(String(100), nullable=False)
    genres=Column(ARRAY(String), nullable=False)
    duration = Column(Integer, nullable=False)
    rating=Column(Float)
    description = Column(String(1000))
    poster_url=Column(String(500))
    added_date=(Column(Date))