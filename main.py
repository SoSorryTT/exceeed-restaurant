import json
from fastapi import FastAPI
from matplotlib.pyplot import table
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder


class Reservation(BaseModel):
    name: str
    time: int
    table_number: int


client = MongoClient('mongodb://localhost', 27018)

# TODO fill in database name
db = client["exceed_restaurant"]

# TODO fill in collection name
collection = db["reserve"]

app = FastAPI()

# TODO complete all endpoint.


@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name: str):
    query = {"name": name}
    r = collection.find(query, {"_id": 0, "name": 1, "time": 1, "table_number": 1})
    listt = list()
    for i in r:
        listt.append(i)
    return {"result": listt}


@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    query = {"table_number": table}
    r = collection.find(query, {"_id": 0, "name": 1, "time": 1, "table_number": 1})
    listt = list()
    for i in r:
        print(i)
        listt.append(i)
    return {"result": listt}


@app.post("/reservation")
def reserve(reservation : Reservation):
    book = jsonable_encoder(reservation)
    query = {'time':book['time'],'table_number':book['table_number']}
    f = collection.find(query)
    for i in f:
        if book['time'] == i['time'] :
            return {"result" : "Can't reserve"}
    collection.insert_one(book)
    return {"result" : "Reserve done"}


@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    n = jsonable_encoder(reservation)
    print(n)
    query = {'time':n['time'],'table_number':n['table_number']}
    new_value = {'$set':query}
    f = collection.find({'$and':[{'time':n['time']},{'table_number':n['table_number']}]})
    # print(type(f))
    print(len(list(f)))
    if len(list(f))==0:
        collection.update_one({'name':n['name']},new_value)
        return {"result": "Update done"}
    return {"result": "Can't update"}


@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number: int):
    query = {'name': name, 'table_number': table_number}
    collection.delete_one(query)
