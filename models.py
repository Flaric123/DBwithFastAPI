from sqlalchemy import Column, Integer, String, ARRAY, Date, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import List
from database import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("movies.id")),
    Column("right_id", ForeignKey("genres.id")),
)

class Genre(Base):  # 1
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))

    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"

class Movie(Base):  # N
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title= Column(String(100), nullable=False)
    year=Column(String(100), nullable=False)
    genres:Mapped[List['Genre']]=relationship(secondary=association_table)
    duration = Column(Integer, nullable=False)
    rating=Column(Float)
    description = Column(String(1000))
    poster_url=Column(String(500))
    added_date=(Column(Date))

    def __repr__(self):
        return f"<Movie(id={self.id}, title='{self.title}', year={self.year})>"
    
class User(Base):
    __tablename__="users"
    
    id = Column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(60), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(), server_default=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, title='{self.username}')>"