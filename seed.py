# вставка начальных данных
from sqlalchemy.orm import Session
from database import engine
from datetime import date
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
with Session(bind=engine) as session:
    u1=models.User(username='user1',password='11111111',email='u1@mail.com')
    u2=models.User(username='user2', password='22222222',email='u2@mail.com')
    u3=models.User(username='user3', password='33333333',email='u3@mail.com')

    g1=models.Genre(name='Триллер')
    g2=models.Genre(name='Вестерн')
    g3=models.Genre(name='Комедия')

    m1=models.Movie(title="The Matrix",
            year=1999,
            genres=[g1],
            duration=100,
            description='научно-фантастический боевик, поставленный братьями Вачовски по собственному сценарию и спродюсированный Джоэлом Сильвером. ',
            rating=8.7,
            added_date=date.today())
    
    m2=models.Movie(title="The Matrix 2",
            year=2004,
            genres=[g2,g1,g3],
            duration=120,
            description='американский научно-фантастический боевик 2003 года, являющийся продолжением фильма «Матрица».',
            rating=7.9,
            added_date=date.today())
    
    m3=models.Movie(title="The Matrix 3",
            year=2020,
            genres=[g3,g2],
            description='американский научно-фантастический боевик, являющийся продолжением фильма «Матрица: Перезагрузка»',
            duration=136,
            rating=6.8,
            added_date=date.today())
    session.add(m2)
    session.add(m1)
    session.add(m3)
    session.add_all([u1,u2,u3])
    session.commit()