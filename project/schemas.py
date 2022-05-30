from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from pydantic.types import conint


class CreateOTP(BaseModel):
    recipient_id: EmailStr


class UserOut(CreateOTP):
    id: int

    created_at: datetime

    class Config:
        orm_mode = True


class CreateUsers(CreateOTP):
    cus_fname: str
    password: str
    cus_id: str


class UserLogin(BaseModel):
    email: EmailStr
    # email: str
    password: str


class Token(BaseModel):
    access_token: str
    user_id: str
    # cus_id: str


class TokenData(BaseModel):
    id: Optional[str] = None


# --------------------------------------------------for otp---


class VerifyOTP(CreateOTP):
    session_id: str
    otp_code: str


class OTPList(VerifyOTP):
    otp_failed_count: int
    status: str


class Verifywithout(CreateOTP):
    recipient_id: str
    otp_code: str


# -----------------------------------seller---

class SellerLogin(BaseModel):
    seller_email: EmailStr
    seller_password: str


class AddSeller(SellerLogin):
    seller_id: str
    # product_id: str


class VerifySeller(BaseModel):
    seller_id: str
    seller_verified: str


# ------------------------------------admin----
class AdminLogin(BaseModel):
    admin_email: EmailStr
    admin_password: str


class AddAdmin(AdminLogin):
    admin_id: str


class VerifyAdmin(BaseModel):
    admin_id: str
    admin_verified: str


# -------------------------------product-------
class AddProduct(BaseModel):
    product_id: str
    product_name: str
    p_qty: int
    p_price: int
    p_color: str
    p_size: str
    category: str
    brand: str
    location: str
    description: str
    discount_amt: str
    available: str
    seller_id: str

    class Config:
        orm_mode = True


# -----loging with customer--
class ShowProduct(BaseModel):
    product_id: str
    product_name: str
    p_color: str
    p_size: str
    p_price: int
    discount_amt: int

    # seller_id: str

    class Config:
        orm_mode = True


# ---------------------------

class UserDash(BaseModel):
    cus_id: str
    cus_dob: str
    cus_phone: str
    cus_region: str
    cus_area: str
    cus_address: str
    gender: str

    class Config:
        orm_mode = True


# class ShowCusid(BaseModel):
#    cus_id: str
#    class Config:
#        orm_mode = True
# -----------------------------order----------
class Order(BaseModel):
    # order_id :str
    cus_id: str
    product_id: str
    product_name: str
    o_qty: int
    p_price: int
    order_verified: str
    discount_amt: int
    delivery_charge: int
    total: int

    class Config:
        orm_mode = True


class OrId(BaseModel):
    order_id: str


# ---------------------working
class Fetch(BaseModel):
    product_id: str
    o_qty: str


# ----------------
class FetchOrder(BaseModel):
    # cus_id: str
    product_id: str
    o_qty: str


class ShowOrder(BaseModel):
    order_id: str
    product_name: str
    total: str

    class Config:
        orm_mode = True


# ------------------for delivery and confirmation
class CusOrder(BaseModel):
    order_id: str
    cus_fname:str
    delivery_loc: str
    phone_no: str
