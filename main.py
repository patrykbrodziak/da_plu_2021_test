from fastapi import FastAPI, HTTPException
import hashlib
from pydantic import BaseModel
import datetime

app = FastAPI()
app.patient_id = 0
app.tab_of_patients = []

####### ZADANIE 1 ###########
@app.get("/")
def root():
    return {'message': 'Hello World!'}

####### ZADANIE 2 ###########
@app.get("/method")
def root_get():
    return {"method": "GET"}

@app.post("/method", status_code=201)
def root_post():
    return {"method": "GET"}

@app.delete("/method")
def root_delete():
    return {"method": "DELETE"}

@app.put("/method")
def root_put():
    return {"method": "PUT"}

@app.options("/method")
def root_options():
    return {"method": "OPTIONS"}

####### ZADANIE 3 ##########
@app.get("/auth")
async def root(password: str, password_hash: str):
    hashed_password = hashlib.sha512(str.encode(password)).hexdigest()
    if password_hash == hashed_password:
        raise HTTPException(status_code=204)
    else:
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
    app.tablica_pacientow.append(patient_dict)
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
