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
def password_auth(response: Response, password: Optional[str] = None, password_hash: Optional[str] = None):
    if not password or not password_hash or hashlib.sha512(str(password).encode("utf-8") ).hexdigest() != str(password_hash):
        raise HTTPException(status_code=401)

#######  ZADANIE 4 #########
class Patient(BaseModel):
    name: str
    surname: str


@app.post("/register", status_code=201)
async def root(patient: Patient):
    app.patient_id += 1
    register_date = datetime.date.today()
    vaccination_date = register_date + datetime.timedelta(onlyLetters(patient.name) + onlyLetters(patient.surname))
    patient_dict = {"id": app.patient_id, "name": patient.name, "surname": patient.surname,
                    "register_date": str(register_date), "vaccination_date": str(vaccination_date)}
    app.tab_of_patients.append(patient_dict)
    return patient_dict

######## ZADANIE 5 #########
@app.get("/patient/{id}")
async def patient_get(id: int):
    if id < 1:
        raise HTTPException(status_code=400)
    elif ((id - 1) >= len(app.tab_of_patients)):
        raise HTTPException(status_code=404)
    return app.tab_of_patients[id - 1]

def onlyLetters(string: str):
    letters = 0
    for letter in string.lower():
        if (letter >= 'a' and letter <='z') or letter in 'ąęóśłżźćń':
            letters += 1
    return letters