from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import User

sec=HTTPBasic()

def auth(credentials: HTTPBasicCredentials=Depends(sec), db: Session=Depends(get_db)):
    foundUser=db.query(User).filter(User.username == credentials.username).first()

    if not foundUser or credentials.password!=foundUser.password:
        raise HTTPException(403, "Неверный логин или пароль")
    
    return foundUser