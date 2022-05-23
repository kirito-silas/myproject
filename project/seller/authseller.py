from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from project import database, schemas, models, utils, oauth2
#from app.database import get_db


router = APIRouter(tags=['AuthenticationSeller'])


@router.post('/sellerlogin', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    b = db.query(models.Seller).filter(models.Seller.seller_verified == '1').delete()
    print(b)
    db.commit()
    user = db.query(models.Seller).filter(models.Seller.seller_email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.seller_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # return token
    access_token = oauth2.create_access_token(data= {"user_id": user.sid})
    return {"access_token": access_token, "user_id": f"{user.seller_id}"}
