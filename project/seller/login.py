from typing import List

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert
from project import models, schemas, utils
from project.adminlog import oauth2admin
from project.database import get_db, database
from project.productspage import oauth2seller

router = APIRouter(
    prefix="/seller",
    tags=['AddSeller']
)


# --------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_202_ACCEPTED)  # , response_model=schemas.UserOut)
async def create_seller(request: schemas.AddSeller, db: Session = Depends(get_db)):
    #adding product id
    #stmt = models.Product(product_id = request.product_id)
    #db.add(stmt)
    #db.commit()
    #db.refresh(stmt)


    # create otp and verify
    seller = db.query(models.Seller).filter(models.Seller.seller_email == request.seller_email).first()
    # ----

    if not seller:


        # hashing password
        hashed_password = utils.hash(request.seller_password)
        request.seller_password = hashed_password

        new_seller = models.Seller(**request.dict())
        db.add(new_seller)
        db.commit()
        db.refresh(new_seller)
        return {"seller_id": request.seller_id,
                "seller_email": request.seller_email,
                "pass": request.seller_password}
    else:
        return {"User already exists!!!!"}
    # return new_user

#------------------ should be able to access only by admin to verify seller-----------now in admin page
#@router.put("/verifyseller", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.UserOut)
#async def verify_seller(request: schemas.VerifySeller, db: Session = Depends(get_db)):
    #print(current_user.admin_id)
    #seller = db.query(models.Seller).filter(models.Seller.seller_id == request.seller_id).first()
    #if seller:
    #seller.seller_verified = request.seller_verified
    #db.commit()
    #print(seller)
    #return {"seller verified"}

