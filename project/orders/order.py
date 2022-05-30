from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert, select
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from typing import Optional, List
from project.orders import random, customerorder
#import random


router = APIRouter(
    prefix="/order",
    tags=['order']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ShowOrder)
async def create_order(newly_made: List[schemas.FetchOrder], db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    #print(current_user.product_id)
    #print(newly_made.cus_id)
    print(current_user.cus_fname)
    cusorder_id = random.randomnumber(10)
    # print(user_id) ,user_id: int= Depends(oauth2.get_current_user())
    #stmt = models.Order(cusorder_id)
    #print(cusorder_id)
    #s = models.Product.select(models.Product.product_name).where(models.Product.product_id == newly_made.product_id)
    print(newly_made)
    for i in newly_made:
        print(i)



        order = db.query(models.Product).filter(models.Product.product_id == i.product_id)
        #a= order.all()
        #print(a)
        #add discount in product later -- DO NOT FORGET
        for row in order:
            print(f"{row.product_name,row.p_price}")
        pname = row.product_name
        pprice = int(row.p_price)
        quantity = int(i.o_qty)
        before_discount = row.p_price * quantity
        discount= row.discount_amt
        delivery_charge = int(100) #can be taken in json script using newlymade.delivery_charge
        tat = before_discount - discount
        tot = tat + delivery_charge

        print(order)
        total = tot+tot
        totalling = customerorder.total(total)
        print(total)
        #cus_id = current_user.cus_id


        stmt = models.Order(order_id = cusorder_id,cus_id=current_user.cus_id,product_id= i.product_id,product_name= pname,o_qty=i.o_qty,p_price=pprice,discount_amt=discount,delivery_charge=delivery_charge,total=tot)
        db.add(stmt)
        db.commit()
        db.refresh(stmt)

    return stmt



    # CODE BELOW IS IN SUSPENSION
    if newly_made.cus_id == current_user.cus_id:

        #newly_made = models.Order(**newly_made.dict())
        #print(newly_made)

        #db.add(newly_made)
        order_query = db.query(models.Order).filter(models.Order.order_id == cusorder_id)  # not id but name
        post = order_query.first()
        order_query.update(order.dict(), synchronize_session=False)

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

