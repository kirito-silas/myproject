from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from project import models
from project.database import engine
from project.routers import user, auth
from project.config import settings
from project.otp import routerotp
from project.database import database
from project.seller import login, authseller
from project.productspage import product
from project.adminlog import admin,authadmin
from project.orders import order,customerorder

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = ["*"]   #for letting websites to access
#check fastapi cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.include_router(googleapi.router)
app.include_router(routerotp.router) #for otp

app.include_router(user.router)
app.include_router(auth.router)
#-----------------------
app.include_router(login.router)
app.include_router(authseller.router)

app.include_router(admin.router)
app.include_router(authadmin.router)
#-------------
app.include_router(product.router)
app.include_router(order.router)
app.include_router(customerorder.router)

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World jk"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
