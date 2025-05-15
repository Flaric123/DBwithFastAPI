# вставка начальных данных
from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
with Session(bind=engine) as session:
    c1 = models.Category(name="Еда")
    session.add(c1)
    p1 = models.Product(name="Яблоко", price=100, category=c1)
    p2 = models.Product(name="Апельсин", price=100, category=c1)
    p3 = models.Product(name="Молоко", price=100, category=c1)
    session.add(p1)
    session.add(p2)
    session.add(p3)
    session.commit()
