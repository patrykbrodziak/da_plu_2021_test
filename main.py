from fastapi import FastAPI, HTTPException, Response, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Optional
import hashlib
from pydantic import BaseModel
import datetime
from functools import wraps
import random

import pytest

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


########### ROZDZIAL 2 ###################
########### ZADANIE 1 ####################
def greetings(funcion):
    def wrapper():
        return 'Hello ' + funcion().title()
    return wrapper

@greetings
def name_surname():
    return "jan nowak"

print(name_surname())
########### ZADANIE 2 #####################
def is_palindrome(function):
    def wrapper():
        word = ''.join(filter(str.isalnum, function())).lower()
        rev = word[::-1]
        if word == rev:
            return function() + " - is palindrome"
        else:
            return function() + " - is not palindrome"
    return wrapper

@is_palindrome
def sentence():
    return "Łapał za kran, a kanarka złapał."


############ ZADANIE 3 #######################
def format_output(*args):
    def decorator(function):
        nonlocal args
        def wrapper():
            nonlocal args
            indict = function()
            outdict = {}
            for arg in args:
                names = arg.split("__")
                val = ""
                for name in names:
                    if name not in indict:
                        raise ValueError()
                    if val != "":
                        val += " "
                    val += indict[name]
                outdict[arg] = val
            return outdict
        return wrapper
    return decorator

@format_output("first_name__last_name", "city")
def first_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }


@format_output("first_name", "age")
def second_func():
    return {
        "first_name": "Jan",
        "last_name": "Kowalski",
        "city": "Warsaw"
    }

########## ZADANIE 4 ################

def add_class_method(cls):
    def decorator(func):
        @classmethod
        @wraps(func)
        def wrapper(self):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


def add_instance_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator

######### WYKLAD 3 #########

security = HTTPBasic()
app.session_token = []
app.token_value = []
app.s_token = []
app.t_token = []
######### ZADANIE 1 ##########

@app.get("/hello", response_class=HTMLResponse)
def hello_function():
    today = datetime.date.today()
    return """<h1>Hello! Today date is {}</h1>""".format(today)

######### ZADANIE 2 ##########
def key():
    return ''.join(random.sample('zxcvbnm,./asdfghjkl;qwertyuiop[]1234567890-=!@#$%^&*()_+)QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?aq', 64))


# @app.post("/login_session", status_code=201)
# def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
#     token = key()
#     if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if token not in app.session_token:
#         if len(app.session_token) >= 3:
#             app.session_token = app.session_token[1:]
#         app.session_token.append(token)
#     response.set_cookie(key="session_token", value=token)
#
#
# @app.post("/login_token", status_code=201)
# def login_token(credentials: HTTPBasicCredentials = Depends(security)):
#     token = key()
#     if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if token not in app.token_value:
#         if len(app.token_value) >= 3:
#             app.session_token = app.session_token[1:]
#         app.token_value.append(token)
#     return {"token": token}

@app.post("/login_session", status_code=201)
def login(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    token = key()
    if token not in app.s_token:
        if len(app.s_token) == 3:
            del app.s_token[0]
        app.s_token.append(token)
    response.set_cookie(key="session_token", value=token)


@app.post("/login_token", status_code=201)
def login_token(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    token = key()
    if token not in app.t_token:
        if len(app.t_token) == 3:
            del app.t_token[0]
        app.t_token.append(token)
    return {"token": token}