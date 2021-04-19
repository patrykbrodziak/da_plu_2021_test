from fastapi import FastAPI, HTTPException
from typing import Optional
import hashlib
from pydantic import BaseModel
import datetime

app = FastAPI()
app.patient_id = 0
app.tab_of_patients = []

####### ZADANIE 1 ###########
@app.get("/")
def root():
    return {'message': 'Hello world!'}

####### ZADANIE 2 ###########
@app.get("/method")
def method_get():
    return {"method": "GET"}

@app.put("/method")
def method_put():
    return {"method": "PUT"}

@app.options("/method")
def method_options():
    return {"method": "OPTIONS"}

@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}

@app.post("/method", status_code=201)
def method_post():
    return {"method": "POST"}

####### ZADANIE 3 ##########
@app.get("/auth", status_code=204)
async def authentication(password: Optional[str] = None, password_hash: Optional[str] = None):
    hashed_password = hashlib.sha512(str.encode(password)).hexdigest()
    if not password or not password_hash or password_hash != hashed_password:
        raise HTTPException(status_code=401)

#######  ZADANIE 4 #########
class Patient(BaseModel):
    name: str
    surname: str

@app.post("/register", status_code=201)
async def root(patient: Patient):
    app.patient_id += 1
    patient = dict(patient)
    register_date = datetime.date.today()
    vaccination_date = register_date + datetime.timedelta(len(patient['name']) + len(patient['surname']))
    patient_dict = {"patient_id": app.patient_id, "name": patient['name'], "surname": patient['surname'], "register_date": register_date,
            "vaccination_date": vaccination_date }
    app.tab_of_patients.append(patient_dict)
    return patient_dict

######## ZADANIE 5 #########
@app.get("/patient/{id}")
async def root_get(id: int):
    patient_id_tab = []
    for i in app.tab_of_patients:
        patient_id_tab.append(i['patient_id'])
    if id in patient_id_tab:
        return app.tab_of_patients[id-1]
    else:
        raise HTTPException(status_code=400)
