from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey, Sequence
from sqlalchemy.sql.expression import null
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from project.database import Base
import datetime
from datetime import datetime

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer,Sequence("users_id_seq"), primary_key=True, nullable=False)
    recipient_id = Column(String, nullable=False, unique=True)
    cus_fname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    verified = Column(String, nullable=False, server_default= '1')
    cus_id = Column(String, ForeignKey("customer.cus_id", ondelete="CASCADE"), primary_key=True)


class otps(Base):
    __tablename__ = "py_otps"
    id = Column(Integer, Sequence("otp_id_seq"), primary_key=True, nullable=False)
    recipient_id = Column(String(100))
    session_id = Column(String(100))
    otp_code = Column(String(6))
    status = Column(String(1))
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    otp_failed_count = Column(Integer)


class otp_blocks(Base):
    __tablename__ = "py_otp_blocks"
    id = Column(Integer, Sequence("otp_id_seq"), primary_key=True, nullable=False)
    recipient_id = Column(String(100))
    created_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#------------------------------------------------------------------------

class Admin(Base):
    __tablename__ = "admin"
    aid = Column(Integer, Sequence("admin_id_seq"), primary_key=True, nullable=False)
    admin_id = Column(String, nullable=False)
    admin_email = Column(String, nullable=False, unique=True)
    admin_password = Column(String, nullable=False)
    admin_verified = Column(String, nullable=False, server_default= '1')

class Seller(Base):
    __tablename__ = "seller"
    sid = Column(Integer, Sequence("seller_id_seq"), primary_key=True, nullable=False)
    seller_id = Column(String, nullable=False)
    seller_email = Column(String, nullable=False, unique=True)
    seller_password = Column(String, nullable=False)
    seller_verified = Column(String, nullable=False, server_default= '1')
    #product_id = Column(String)
    #owner = relationship("Users")

class Product(Base):
    __tablename__ = "product"
    pid = Column(Integer, Sequence("product_id_seq"),primary_key=True, nullable=False)
    product_id = Column(String, nullable=False)
    #product_id = Column(String, nullable=False, unique=True)
    product_name = Column(String)
    p_qty = Column(Integer)
    p_price = Column(String)
    p_color = Column(String)
    p_size = Column(String)
    category = Column(String)
    brand = Column(String)
    location = Column(String)
    description = Column(String)
    available = Column(String)
    #sid = Column(Integer, ForeignKey("seller.sid", ondelete="CASCADE"), nullable=False)
    #seller_id = relationship("Seller")
    seller_id = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Customer(Base):
    __tablename__ = "customer"
    cus_id = Column(String, primary_key=True, nullable=False, unique=True)
    cus_fname = Column(String)
    cus_email = Column(String)
    cus_dob = Column(String)
    cus_phone = Column(String)
    cus_region = Column(String)
    cus_area = Column(String)
    cus_address = Column(String)
    gender = Column(String)
    #cus_verified = Column(String, nullable=False, server_default= '1')
    #recipient_id = Column(String, ForeignKey("users.recipient_id", ondelete="CASCADE"), primary_key=True)
    #seller_id = Column(String, ForeignKey("seller.seller_id", ondelete="CASCADE"), primary_key=True)

class Order(Base):
    __tablename__ = "order"
    oid = Column(Integer, Sequence("order_id_seq"), primary_key=True, nullable=False)
    order_id = Column(String)
    cus_id = Column(String, ForeignKey("customer.cus_id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(String)
    product_name = Column(String)
    o_qty = Column(Integer, nullable=False)
    p_price = Column(Integer, nullable=False)
    order_verified = Column(String, nullable=False, server_default= '1')
    discount_amt = Column(Integer)
    delivery_charge = Column(Integer)
    total = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class CusOrder(Base):
    __tablename__ = "customerorder"
    cus_order_id = Column(String, primary_key=True, nullable=False, unique=True)
    order_id = Column(String)
    cus_id = Column(String)
    cus_fname = Column(String)
    delivery_loc = Column(String, nullable=False)
    phone_no = Column(Integer, nullable=False)

class OrderReport(Base):
    __tablename__ ="orderreport"
    order_report_id = Column(String, Sequence("auto_order"), primary_key=True, nullable=False)
    cus_order_id = Column(String, ForeignKey("customerorder.cus_order_id", ondelete="CASCADE"), primary_key=True)
    order_id = Column(String)
    cus_id = Column(String)
    product_id = Column(String)
    product_name = Column(String)
    o_qty = Column(String)
    order_verified = Column(String)
    total = Column(String)
    created_at = Column(String)

class Discount(Base):
    __tablename__ = "discount"
    discount_id = Column(String, primary_key =True, nullable=False)
    discount_amt = Column(Integer)
    expiry_date = Column(Integer)

class Eligible(Base):
    __tablename__ = "eligible"
    eli_id = Column(String, primary_key= True, nullable=False)
    discount_id = Column(String, ForeignKey("discount.discount_id", ondelete="CASCADE"), primary_key=True)
    cus_id = Column(String, ForeignKey("customer.cus_id", ondelete="CASCADE"), primary_key=True)

class Onc(Base):
    __tablename__ = "onc"
    onc_id = Column(String, primary_key=True, nullable=False, unique=True)
    order_id = Column(String)
    cus_id = Column(String, ForeignKey("customer.cus_id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(String)
    product_name = Column(String)
    o_qty = Column(String)
    order_verified = Column(String)
    total = Column(String)
    created_at = Column(String)

class Wishlist(Base):
    __tablename__ ="wishlist"
    wish_id = Column(String, primary_key = True, nullable=False)
    cus_id = Column(String, ForeignKey("customer.cus_id", ondelete="CASCADE"), primary_key=True)
    onc_id = Column(String, ForeignKey("onc.onc_id", ondelete="CASCADE"), primary_key=True)




#----------------------------------------------------tries
