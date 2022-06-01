from project.productspage import productpic
from fastapi import FastAPI, UploadFile, File, APIRouter, Depends
from sqlalchemy.orm import Session
import shutil
from project.orders import random
from project.database import get_db
from project import models, schemas, utils, oauth2

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


def uploadimage(file: UploadFile = File(...)):
    with open(f'{file.filename}', "wb") as buffer:
        productpic.copyfileobj(file.file, buffer)
