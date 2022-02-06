from fastapi import FastAPI
from matplotlib.pyplot import table
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["exceed_restaurant"]

# TODO fill in collection name
collection = db["reservation"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    query = {"name":name}
    r = collection.find(query,{"_id":0,"name":1,"time":1,"table_number":1})
    listt = list()
    for i in r:
        listt.append(i)
    return {"result":listt}

@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    query = {"table_number":table}
    r = collection.find(query,{"_id":0,"name":1,"time":1,"table_number":1})
    listt = list()
    for i in r:
        listt.append(i)
    return {"result":listt}

@app.post("/reservation")
def reserve(reservation : Reservation):
    pass

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    query = {'name':name,'table_number':table}
    collection.delete_one(query)