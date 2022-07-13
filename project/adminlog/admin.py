from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert
from project import models, schemas, utils
from project.adminlog import oauth2admin
from project.database import get_db, database


router = APIRouter(
    prefix="/admin",
    tags=['Addadmin']
)


# --------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_202_ACCEPTED)  # , response_model=schemas.UserOut)
async def create_admin(request: schemas.AddAdmin, db: Session = Depends(get_db)):

    # create otp and verify
    seller = db.query(models.Admin).filter(models.Admin.admin_email == request.admin_email).first()
    if not seller:


        # hashing password
        hashed_password = utils.hash(request.admin_password)
        request.admin_password = hashed_password

        new_admin = models.Admin(**request.dict())
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return {"seller_id": request.admin_id,
                "seller_email": request.admin_email}
    else:
        return {"User already exists!!"}
    # return new_user

#------------------ should be able to access only by admin to verify seller-----------
@router.put("/verifyadmin", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.UserOut)
async def verify_admin(request: schemas.VerifyAdmin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.admin_id == request.admin_id).first()
    #if seller:
    admin.admin_verified = request.admin_verified
    db.commit()
    print(admin)
    return {"admin verified"}

@router.put("/verifyseller", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.UserOut)
async def verify_seller(request: schemas.VerifySeller, db: Session = Depends(get_db), current_user: str = Depends(oauth2admin.get_current_user)):
    print(current_user.admin_id)
    seller = db.query(models.Seller).filter(models.Seller.seller_id == request.seller_id).first()
    #if seller:
    seller.seller_verified = request.seller_verified
    db.commit()
    print(seller)
    return {"seller verified"}
