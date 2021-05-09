from fastapi import FastAPI, HTTPException, Response, Depends, status, Cookie
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, RedirectResponse
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Optional
import hashlib
from pydantic import BaseModel
import datetime
from functools import wraps
import secrets
import random
import sqlite3
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

app.session_token = []
app.token_value = []

random.seed(datetime.datetime.now())

@app.post("/login_session", status_code=201)
def login_session(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "4dm1n" or credentials.password != "NotSoSecurePa$$":
        raise HTTPException(status_code=401)
    secret_number = str(random.randint(0, 100000000))
    session_token = hashlib.sha256("{}{}{}".format(credentials.username, credentials.password, secret_number).encode()).hexdigest()
    response.set_cookie(key="session_token", value=session_token)
    if len(app.session_token) >= 3:
        app.session_token = app.session_token[1:]
    app.session_token.append(session_token)
    return {"OK"}


@app.post("/login_token", status_code=201)
def login_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "4dm1n")
    correct_password = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not(correct_password and correct_username):
        raise HTTPException(status_code=401)
    secret_number = str(random.randint(0, 100000000))
    session_token = hashlib.sha256("{}{}{}".format(credentials.username, credentials.password, secret_number).encode()).hexdigest()
    if len(app.token_value) >= 3:
        app.token_value = app.token_value[1:]
    app.token_value.append(session_token)
    return {"token": session_token}
#
@app.get("/welcome_session")
def welcome_session(format:str = "", session_token: str = Cookie(None)):
    if session_token not in app.session_token:
        raise HTTPException(status_code=401)
    if format == "json":
        return {"message": "Welcome!"}
    if format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
    return PlainTextResponse(content="Welcome!", status_code=200)

@app.get("/welcome_token")
def welcome_token(token: str = "", format: str = ""):
    if (token == "") or (token not in app.token_value):
        raise HTTPException(status_code=401)
    if format == "json":
        return {"message": "Welcome!"}
    if format == "html":
        return HTMLResponse(content="<h1>Welcome!</h1>", status_code=200)
    return PlainTextResponse(content="Welcome!", status_code=200)

@app.delete("/logout_session")
def logout_session(format:str = "", session_token: str = Cookie(None)):
    if session_token not in app.session_token:
        raise HTTPException(status_code=401)

    app.session_token.remove(session_token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=303)



@app.delete("/logout_token")
def logout_token(token: str = "", format: str = ""):
    if (token == "") or (token not in app.token_value):
        raise HTTPException(status_code=401)

    app.token_value.remove(token)
    url = "/logged_out?format=" + format
    return RedirectResponse(url=url, status_code=303)


@app.get("/logged_out", status_code=200)
def logged_out(format:str = ""):
    if format == "json":
        return {"message": "Logged out!"}
    elif format == "html":
        return HTMLResponse(content="<h1>Logged out!</h1>", status_code=200)
    else:
        return PlainTextResponse(content="Logged out!", status_code=200)



############ WYKLAD 4 ##############
############ ZADANIE 1 #############
# @app.on_event("startup")
# async def startup():
#     app.db_connection = sqlite3.connect("northwind.db", check_same_thread=False)
#     app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     app.db_connection.close()


@app.get("/categories", status_code=200)
async def categories():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")
    app.db_connection.row_factory = sqlite3.Row
    categoriess = app.db_connection.execute('''
    SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID
    ''').fetchall()
    app.db_connection.close()
    return {"categories": [{"id": "{}".format(i['CategoryID']), "name": "{}".format(i["CategoryName"])} for i in categoriess]}

@app.get("/customers", status_code=200)
async def customers():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")
    app.db_connection.row_factory = sqlite3.Row
    customerss = app.db_connection.execute('''
    SELECT CustomerID, CompanyName, (COALESCE(Address, '') || ' ' || COALESCE(PostalCode, '') || ' ' || COALESCE(City, '') || ' ' || COALESCE(Country, '')) AS full_address FROM Customers ORDER BY CustomerID
    ''').fetchall()
    app.db_connection.close()
    return {"customers": [{"id": "{}".format(i['CustomerID']), "name": "{}".format(i["CompanyName"]), "full_address": "".format(i["full_address"])} for i in customerss]}


# @app.get("/customers")
# async def customers():
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         """SELECT CustomerId AS id, CompanyName AS name,
#           Address || ' ' || PostalCode || ' ' || City || ' ' || Country AS full_address FROM customers""").fetchall()
#     return {
#         'customers': data
#     }
#
# @app.get("/categories")
# async def categories_list():
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         "SELECT CategoryId AS id, CategoryName AS name FROM Categories").fetchall()
#     return {
#         'categories': data
#     }