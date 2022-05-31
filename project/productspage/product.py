from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from typing import Optional, List

from project.productspage import oauth2seller

router = APIRouter(
    prefix="/product",
    tags=['product']
)


# --------------------------------------------------------------------------


@router.get("/seller", response_model=List[schemas.ShowProduct])
async def sellerproduct(db: Session = Depends(get_db), current_user: str = Depends(oauth2seller.get_current_user), limit: int = 10,
                   skip: int = 0, search: Optional[str] = ""):
    print(current_user.seller_email)
    # cursor.execute(""""SELECT * FROM post """)
    #'''cursor.execute("""SELECT * FROM post""")
    #posti = cursor.fetchall()
    #print(posti)'''
    product = db.query(models.Product).filter(models.Product.product_name.contains(search), models.Product.seller_id == current_user.seller_id).limit(limit).offset(skip).all()
    #product = db.query(models.Product).all()
    return product

@router.get("/", response_model=List[schemas.ShowProduct])
async def allproduct(db: Session = Depends(get_db), limit: int = 10,
                   skip: int = 0, search: Optional[str] = ""):
    #print(current_user.recipient_id)
    # cursor.execute(""""SELECT * FROM post """)
    #'''cursor.execute("""SELECT * FROM post""")
    #posti = cursor.fetchall()
    #print(posti)'''
    product = db.query(models.Product).filter(models.Product.product_name.contains(search), models.Product.available == 'yes', models.Product.p_qty != '0').limit(limit).offset(skip).all()
    #product = db.query(models.Product).all()

    return product



'''@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
'''

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AddProduct)
async def create_product(newly_made: schemas.AddProduct, db: Session = Depends(get_db), current_user: str = Depends(oauth2seller.get_current_user)):
    #print(current_user.product_id)
    print(current_user.seller_id)
    #print(user_id) ,user_id: int= Depends(oauth2.get_current_user())
    

    #newly_made = models.Product(seller_id=current_user.seller_id, **newly_made.dict())
    if newly_made.seller_id == current_user.seller_id:
        newly_made = models.Product(**newly_made.dict())
        print(newly_made)
        db.add(newly_made)
        db.commit()
        db.refresh(newly_made)
        return newly_made
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
        print("not authroized seller")
        return {"Unauthorized"}


@router.get("/{id}", response_model=schemas.ShowProduct)
async def retrivefromid(id: str, db: Session = Depends(get_db)):
    #print(user_id)
    '''cursor.execute("""SELECT * FROM post WHERE id = %s""", (str(id)))
    posting = cursor.fetchone()'''
    posting = db.query(models.Product).filter(models.Product.product_name == id).first()
    print(posting)
    if not posting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {id} was not found")
        '''response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": f"the id {id} was not found"}
        '''

    print(posting)
    return posting


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletefromid(id: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2seller.get_current_user)):
    '''cursor.execute("""DELETE FROM post WHERE id = %s returning *""", (str(id)))
    deletefromid = cursor.fetchone()
    conn.commit()'''
    delte_query = db.query(models.Product).filter(models.Product.product_id == id)
    delte = delte_query.first()

    if delte_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {id} does not exist")

    if delte.seller_id != current_user.seller_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
    delte_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.AddProduct)
async def updatefromid(id: str, updatepost: schemas.AddProduct, db: Session = Depends(get_db),current_user: str = Depends(oauth2seller.get_current_user)):

    if updatepost.seller_id == current_user.seller_id:
        post_query = db.query(models.Product).filter(models.Product.product_name == id) #not id but name
        post = post_query.first()

        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {id} does not exist")
        # newly_made = models.Post(**newly_made.dict())
        if post.seller_id != current_user.seller_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")

        post_query.update(updatepost.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
        print("not authroized seller")
        return {"Unauthorized"}

