
from project import models, schemas, utils, oauth2
from project.database import get_db, database

import random

import string
def randomnumber(S):
    result1 = ''.join((random.choice(string.ascii_uppercase) for x in range(S)))
    return result1

def update_order_id(request: schemas.OrId):
    print(request.order_id)
    #see crud lifetime for proper view
    query = "UPDATE order SET order_id=request.result1 where cus_id = request.cus_id "
    return database.execute(query, values={"order_id": request.order_id})