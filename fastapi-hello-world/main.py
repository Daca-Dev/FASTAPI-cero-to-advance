# python
from os import path
from typing import Optional
from enum import Enum # nos permite crear enumeraciones 
# pydantic
from pydantic import (
    BaseModel, Field, EmailStr
)
# fastapi
from fastapi import (
    FastAPI, Body, Query,
    Path, status, Form,
    Header, Cookie, UploadFile,
    File, HTTPException
)


app = FastAPI()

# enums
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

# models
class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='David'
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Casas'
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=26
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=False)
    
class Person(PersonBase):
    password: str = Field(..., min_length=8)
    
    # las validaciones de request body se hacen en el modelo
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "David",
    #             "last_name": "Casas",
    #             "age": "26",
    #             "hair_color": "black",
    #             "is_married": "false"
    #         }
    #     }
    
class PersonOut(PersonBase):
    pass # Keyword de python que dice que no se hace nada

class Location(BaseModel):
    city: str = Field(..., min_length=3)
    state: str = Field(..., min_length=3)
    country: str = Field(..., min_length=3)

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='Daca1953')
    messagge: str = Field(default='Login Succesfull')


# path operation: es un decorador que define el método
# que se usará
# - el parametro pasado e
@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=['Home',]
    )
def home():
    return {
        'hello': 'world'
    }


# request and response body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=['Persons',],
    summary= "Create person in the app"# titulo personalisado para el path operation
    )
def create_person(person: Person=Body(...)): # el ... significa que el parametro es obligatorio
    """
    # Create person
    
    This path operation create a person in the app and save the information in the database
    
    Parameters:
    - Request Body parameter:
        - **person: Person** -> A person model with first name, last name, age, haur color and if is married
    
    Return a person model with first name, last name, age, hair color and marital status
    """
    return person


# validaciones query parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK,
    tags=['Persons',],
    deprecated=True
    )
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title = 'Personal name',
        description = "This is the person name. It's between 1 and 50 characters.",
        example = 'Bender'
        ),
    age: str = Query(
        ...,
        title = 'Personal age',
        description = "This is the person age. It's required.",
        example = 26
        )
):
    return {name: age}


# validatiosn: path parameters

persons = [1,2,3,4,5] # personas registradas

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Persons',]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title = 'Person ID',
        description = "This is the ID of person register in Data Base",
        example = 123
    )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "This person Doesn't exist" # mensaje del error
        )
    
    return {
        person_id: "it exists!"
    }
    

# validations: request body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Persons',]
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example = 110# greather tha 0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    return person

# Formularios
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Home',]
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)

# Cookies and headers parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=['Home',]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    # parametros de headers
    user_agent: Optional[str] = Header(default=None), # cabecera que nos dice quien esta trantando de usar el endpoint
    asd: Optional[str] = Cookie(default=None)
):
    return user_agent

# Files
@app.post(
    path='/post-image',
    status_code=status.HTTP_200_OK,
    tags=['Files',]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(KB)": round(len(image.file.read()) / 1024, ndigits=2)
    }