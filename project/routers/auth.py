from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from project import database, schemas, models, utils, oauth2
#from app.database import get_db


router = APIRouter(tags=['Authentication'])


@router.post('/user/login', response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    b = db.query(models.Users).filter(models.Users.verified == '1').delete()
    print(b)
    db.commit()
    #deleting customer if not verified
    cus = db.query(models.Customer).filter(models.Customer.cus_email == None).delete()
    print(cus)
    db.commit()

    user = db.query(models.Users).filter(models.Users.recipient_id == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")



    #printing in backend only
    print(user.cus_id)
    #await read_users_me(user.cus_id)

    # return token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    return {"access_token": access_token, "user_id": f"{user.cus_id}"}

#-------------------loggout-----
#@router.put("/user/logout")
#async def modifypassword(request: schemas.ForgotPass, db: Session = Depends(get_db)):