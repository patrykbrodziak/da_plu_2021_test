from fastapi import FastAPI, HTTPException, Response
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
async def authentication(response: Response, password: Optional[str], password_hash: Optional[str]):
    hashed_password = hashlib.sha512(str.encode(password)).hexdigest()
    if not password or not password_hash or hashed_password != str(password_hash):
        raise HTTPException(status_code=401)

#######  ZADANIE 4 #########
class Patient(BaseModel):
    name: str
    surname: str

class SavedPatient(BaseModel):
    id: int
    name: str
    surname: str
    register_date: str
    vaccination_date: str

@app.post("/register", status_code=201, response_model=SavedPatient)
async def root(patient: Patient):
    app.patient_id += 1
    register_date = datetime.date.today()
    vaccination_date = register_date + datetime.timedelta(len(patient.name) + len(patient.surname))
    patient_dict = {"id": app.patient_id, "name": patient.name, "surname": patient.surname,
                    "register_date": str(register_date), "vaccination_date": str(vaccination_date)}
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
