from typing import List, Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import delete, update, insert
from project import models, schemas, utils, oauth2
from project.database import get_db, database
from project.otp import routerotp, otp
from starlette.responses import RedirectResponse
# -------------------------
from project.otp import otp, crud, otpUtil, foremail
import uuid
from project.database import database
from project.orders import random
from project.productspage import uploadimg
# --------------------

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# --------------------------------------------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.UserOut)
async def create_user(request: schemas.CreateUsers, db: Session = Depends(get_db)):
    # adding  cus_id in customer
    customerid = random.randomnumber(10)
    cusid = "CUS-" + customerid
    stmt = models.Customer(cus_id=cusid, cus_email=request.recipient_id, cus_fname=request.cus_fname)
    db.add(stmt)
    db.commit()
    db.refresh(stmt)

    # for profile pic
    #await uploadimg.create_file(cusid)   --- doesnot work

    # create otp and verify
    user = db.query(models.Users).filter(models.Users.recipient_id == request.recipient_id).first()
    if not user:

        otp_blocks = await crud.find_otp_block(request.recipient_id)
        if otp_blocks:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Sorry, this phone will be blocked in 5 min")

        # generate and save in py_otps table
        otp_code = otpUtil.random(6)
        session_id = str(uuid.uuid1())
        await crud.save_otp(request, session_id, otp_code)
        foremail.sendemail(request.recipient_id, otp_code)

        # await routerotp.send_otp(user.email, user.email)

        # hashing password
        hashed_password = utils.hash(request.password)
        request.password = hashed_password

        # new_user = models.Users(**request.dict())
        new_user = models.Users(recipient_id=request.recipient_id, cus_fname=request.cus_fname,
                                password=request.password, cus_id=cusid)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # adding email to customer table ok

        return {"recipient_id": request.recipient_id,
                "session_id": session_id,
                "otp_code": otp_code}
    else:
        return {"User already exists!!"}
    # return new_user


@router.post("/verify")
async def send_verify(request: schemas.VerifyOTP, db: Session = Depends(get_db)):
    user = request.recipient_id
    # new_user = models.Users(user)

    otp_blocks = await crud.find_otp_block(request.recipient_id)
    if otp_blocks:
        b = db.query(models.Users).filter(models.Users.verified == '1').delete()
        print(b)
        db.commit()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sorry, this phone will be blocked in 5 min")

    # check otp lifespan
    lifetime_result = await crud.find_otp_lifetime(request)
    if not lifetime_result:
        b = db.query(models.Users).filter(models.Users.verified == '1').delete()
        print(b)
        db.commit()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="OTP code has expired, please request a new one")

    lifetime_result = schemas.OTPList(**lifetime_result)
    print(lifetime_result)

    # check if OTP code is already used
    if lifetime_result.status == "9":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="OTP code has been used, please request a new one")

    # verify OTP code
    if lifetime_result.otp_code != request.otp_code:
        await crud.update_otp_failed_count(lifetime_result)
        # increment OTP failed count
        # then block otp
        if lifetime_result.otp_failed_count + 1 == 5:
            await crud.save_block_otp(lifetime_result)
            b = db.query(models.Users).filter(models.Users.verified == '1').delete()
            print(b)
            db.commit()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Failed")
        b = db.query(models.Users).filter(models.Users.verified == '1').delete()
        print(b)
        db.commit()
        # throw exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The OTP code you've entered is incorrect.")

    # disable OTP when success verified

    await crud.disable_otp_code(lifetime_result)
    # add user
    # changing values
    a = db.query(models.Users).filter(models.Users.recipient_id == request.recipient_id).first()
    print(a)
    a.verified = '0'
    db.commit()

    return {
        "status_code": status.HTTP_200_OK,
        "detail": "OTP verified successfully"
    }


@router.get("/{id}", response_model=schemas.UserOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exists")
    return user


# --------------------------------------dashboard--------

# ---adiing details
@router.put("/dashboard/", response_model=schemas.UserDash)
async def updatefromuser(updatepost: schemas.UserDash, db: Session = Depends(get_db),
                         current_user: str = Depends(oauth2.get_current_user)):
    print(current_user.cus_id)
    # print(updatepost.cus_id)
    if updatepost.cus_id == current_user.cus_id:
        # if models.Customer.cus_id == current_user.cus_id:
        post_query = db.query(models.Customer).filter(models.Customer.cus_id == current_user.cus_id)  # not id but name
        post = post_query.first()
        print(post.cus_id)

        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the id {post.cus_id} does not exist")
        # newly_made = models.Post(**newly_made.dict())
        if post.cus_id != current_user.cus_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"not authorized to perform request actions")

        post_query.update(updatepost.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"not authorized to perform request actions")
        print("not authroilzed")
        return {"Unauthorized"}


# ------------------------showing personal details----------
@router.get("/dashboard/")
async def personaldetails(db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    product = db.query(models.Customer).filter(models.Customer.cus_id == current_user.cus_id).all()
    # product = db.query(models.Product).all()
    return product


# ----------------------------forgot password-------
@router.put("/forgotpass")
async def modifypassword(request: schemas.ForgotPass, db: Session = Depends(get_db)):
    print("hello")

    user = db.query(models.Users).filter(models.Users.recipient_id == request.recipient_id).first()
    print(user.recipient_id)

    if user:
        hashed_password = utils.hash(request.password)
        request.password = hashed_password
        # print(request.password)

        # user.update(**request.dict(), synchronize_session=False)
        user.password = request.password
        db.commit()
        db.refresh(user)
        return {"Password changed"}
    else:
        return {"User does not already exists!!"}
