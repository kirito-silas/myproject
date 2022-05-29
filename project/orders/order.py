from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from typing import Optional, List
from project.orders import random
#import random

import string
from project.productspage import oauth2seller

router = APIRouter(
    prefix="/order",
    tags=['order']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Order)
async def create_order(newly_made: schemas.Order, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    #print(current_user.product_id)
    print(newly_made.cus_id)
    print(current_user.cus_fname)
    cusorder_id = random.randomnumber(10)
    # print(user_id) ,user_id: int= Depends(oauth2.get_current_user())
    #stmt = models.Order(cusorder_id)
    #print(cusorder_id)
    stmt = models.Order(order_id = cusorder_id,cus_id=current_user.cus_id,product_id= 0,product_name= 0,o_qty=0,p_price=0,discount_amt=0,delivery_charge=0,total=0)
    db.add(stmt)
    db.commit()
    db.refresh(stmt)



    # newly_made = models.Product(seller_id=current_user.seller_id, **newly_made.dict())
    if newly_made.cus_id == current_user.cus_id:

        #newly_made = models.Order(**newly_made.dict())
        #print(newly_made)

        #db.add(newly_made)
        order_query = db.query(models.Order).filter(models.Order.order_id == cusorder_id)  # not id but name
        post = order_query.first()
        order_query.update(newly_made.dict(), synchronize_session=False)

        db.commit()
        #db.refresh(newly_made)





        return newly_made
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
        print("not authroized seller")
        return {"Unauthorized"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteorder(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):

    delte_query = db.query(models.Order).filter(models.Order.order_id == id)
    delte = delte_query.first()

    if delte_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {id} does not exist")

    if delte.cus_id != current_user.cus_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
    delte_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

