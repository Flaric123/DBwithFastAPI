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


@app.post("/product")
def CreateProduct(Product: PYD.CreateProduct, db: Session = Depends(get_db)):
    cat_db = (
        db.query(models.Category)
        .filter(models.Category.id == Product.category_id)
        .first()
    )
    if not cat_db:
        raise HTTPException(404, "Такой категории нет")
    p1 = models.Product()
    p1.name = Product.name
    p1.price = Product.price
    p1.category = cat_db
    db.add(p1)
    db.commit()
    return p1


@app.get("/product", response_model=List[PYD.SchemeProduct])
def GetProduct(db: Session = Depends(get_db)):
    p1 = db.query(models.Product).all()
    return p1


@app.post("/product/image/{product_id}", response_model=PYD.SchemeProduct)
def upload_image(product_id: int, image: UploadFile, db: Session = Depends(get_db)):
    product_db = (
        db.query(models.Product).filter(models.Product.id == product_id).first()
    )
    if not product_db:
        raise HTTPException(404)
    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, "Неверный тип данных")
    with open(f"files/{image.filename}", "wb") as f:
        shutil.copyfileobj(image.file, f)
    product_db.img = f"files/{image.filename}"
    db.commit()
    return product_db
