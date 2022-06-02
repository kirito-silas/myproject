from starlette import status

from project.productspage import productpic, oauth2seller
from fastapi import FastAPI, UploadFile, File, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
from project.orders import random
from project.database import get_db
from project import models, schemas, utils, oauth2
from typing import List

router = APIRouter(
    prefix="/uploadfile",
    tags=['uploadfile']
)


@router.post('/')
async def create_file(file: UploadFile = File(...)):
    print(id)
    a = random.randomnumber(4)  # increase if not more random alphabets are needed
    image = a + '-' + file.filename
    with open(f'project/productspage/productpic/{image}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"file_name": image}


@router.post('/profilepic')
async def create_file(file: UploadFile = File(...),db: Session = Depends(get_db),
                         current_user: str = Depends(oauth2.get_current_user)):

    print(current_user.cus_id)
    a = random.randomnumber(4)# increase if not more random alphabets are needed
    image = a +'-'+file.filename
    with open(f'project/productspage/productpic/{image}', "wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    stmt = models.Picture(user_n_product_id=current_user.cus_id,pic_id=image )
    db.add(stmt)
    db.commit()
    db.refresh(stmt)

    return {"file_name": image}


@router.post('/addproductpic/{id}')
async def create_file(id: str, files: List[UploadFile] = File(...),db: Session = Depends(get_db),
                         current_user: str = Depends(oauth2seller.get_current_user)):
    print(id)
    for img in files:
        id = id

        print(current_user.seller_id)
        randomid = random.randomnumber(50)
        a = random.randomnumber(4)# increase if not more random alphabets are needed
        image = a +'-P'+img.filename
        with open(f'project/productspage/productpic/{image}', "wb") as buffer:
            shutil.copyfileobj(img.file,buffer)

        stmt = models.ProductPictureZ(id=randomid, product_id=id, pic_id=image)
        db.add(stmt)
        db.commit()
        db.refresh(stmt)



    return {"file_name added"}

@router.post('/getpictures/{id}')
async def findpic(id: str, db: Session = Depends(get_db)):
    picture = db.query(models.ProductPicture).filter(models.ProductPicture.product_id == id)
    print(picture)
    if not picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {id} was not found")
    s=""
    for row in picture:
        #print(f"{row.pic_id}")
        a= row.pic_id + " , "
        s += a
        print(s)
    return{f'project/productspage/productpic/{s}'}



