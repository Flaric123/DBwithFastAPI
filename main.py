from fastapi import FastAPI, HTTPException, Depends, File, Form, UploadFile
import models
import PYD
from database import get_db
from typing import List
from sqlalchemy.orm import Session
import shutil
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/files", StaticFiles(directory="files"), name="files")

@app.get('/movies', response_model=List[PYD.MovieReturn])
def GetMovies(db: Session = Depends(get_db)):
    p1=db.query(models.Movie).all()
    for i in p1:
        print(i)
    return p1

@app.get('/movies/{movie_id}',response_model=PYD.MovieReturn)
def GetMovieById(movies_id: int, db: Session = Depends(get_db)):
    movie_db=(
        db.query(models.Movie).filter(models.Movie.id==movies_id).first()
    )
    if not movie_db:
        raise HTTPException(404, 'Фильма с таким id нет.')
    return movie_db

@app.put('/movies/{movies_id}',response_model=PYD.MovieReturn)
def UpdateMovie(movie_id:int, updateData: PYD.MovieUpdate, db: Session = Depends(get_db)):
    m1=db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not m1:
        raise HTTPException(404, 'Фильма с таким id нет')
    
    for field,value in updateData.model_dump(exclude={'genres'}, exclude_unset=True).items():
        setattr(m1, field, value)

    if updateData.genres:
        genres = db.query(models.Genre).filter(models.Genre.id.in_(updateData.genres)).all()

        if len(genres) != len(updateData.genres):
            raise HTTPException(400, 'Не удалось найти жанры по указанным id')
        
        m1.genres=genres
    
    db.commit()
    db.refresh(m1)

    return m1

@app.delete('/movies/{movies_id}', response_model=PYD.MovieReturn)
def DeleteMovie(movie_id:int, db:Session=Depends(get_db)):
    m1 = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not m1:
        raise HTTPException(404, "Фильм с таким id не найден")

    db.delete(m1)
    db.commit()

    return m1

@app.put("/movies/{movie_id}/image", response_model=PYD.MovieReturn)
def UploadMoviePoster(movie_id:int, image: UploadFile, db:Session=Depends(get_db)):
    m1=db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if not m1:
        raise HTTPException(404, "Фильм с таким id не найден")
    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Неверный тип данных")
    
    maxSize=5
    image.file.seek(0,2)
    imageSize=image.file.tell()
    image.file.seek(0)

    if imageSize>maxSize * 1024*1024:
        raise HTTPException(400, f'Ваш размер: {imageSize}, Максимальный размер: {maxSize}')

    with open(f'files/{image.filename}', "wb") as f:
        shutil.copyfileobj(image.file, f)

    m1.poster_url=f'files/{image.filename}'
    db.commit()
    return m1

@app.post("/movies", response_model=PYD.MovieReturn)
def CreateMovie(createData: PYD.MovieCreate, db: Session = Depends(get_db)):
    genre_query=db.query(models.Genre).filter(models.Genre.id.in_(createData.genres)).all()

    if len(genre_query) != len(createData.genres):
      raise HTTPException(400, "Не удалось найти жанры по указанным id")

    m1=models.Movie(**createData.model_dump(exclude={"genres"}))
    m1.genres=genre_query

    db.add(m1)
    db.commit()
    db.refresh(m1)
    return m1

@app.get('/genres',response_model=List[PYD.GenreCreate])
def GetGenres(db: Session = Depends(get_db)):
    p1=db.query(models.Genre).all()
    return p1

@app.post("/genres")
def CreateGenre(createData: PYD.GenreCreate, db: Session = Depends(get_db)):
    genre_query=db.query(models.Genre).filter(models.Genre.name == createData.name).all()

    if genre_query:
        raise HTTPException(400, "Жанр с таким названием уже существует")

    g1=models.Genre(**createData.model_dump())
    db.add(g1)
    db.commit()
    db.refresh(g1)
    return g1

@app.post('/users',responseModel=PYD.UserReturn)
def CreateUser(createData: PYD.UserCreate, db: Session = Depends(get_db)):
    foundUser = db.query(models.User).filter(models.User.username == createData.username).first()

    if foundUser:
        raise HTTPException(400, "Пользователь с таким именен уже существует")
  
    u1 = models.User(**createData.model_dump())
    db.add(u1)
    db.commit()

    return u1