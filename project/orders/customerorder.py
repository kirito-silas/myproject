from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert, select
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from typing import Optional, List
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from project.orders import random

router = APIRouter(
    prefix="/delivery",
    tags=['delivery']
)


def total(a):
    global A
    A = a

    print("hello ",A)



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_delivery(newly_made: schemas.CusOrder, db: Session = Depends(get_db),current_user: str = Depends(oauth2.get_current_user)):
    print(newly_made)
    #print(A)
    print(current_user.cus_id)
    delivery_order_id = random.randomnumber(10)
    locid = "DEL" + delivery_order_id

    customer_name = db.query(models.Product).filter(models.Customer.cus_id == current_user.cus_id)

    stmt = models.CusOrder(cus_order_id=locid ,order_id=newly_made.order_id ,cus_id=current_user.cus_id,cus_fname=newly_made.cus_fname,
                           delivery_loc=newly_made.delivery_loc,phone_no=newly_made.phone_no,total = 100)
    db.add(stmt)
    db.commit()
    db.refresh(stmt)
    return stmt



