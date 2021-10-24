# python
from os import path
from typing import Optional
from enum import Enum # nos permite crear enumeraciones
# pydantic
from pydantic import BaseModel, Field
# fastapi
from fastapi import FastAPI, Body, Query, Path, status


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



# path operation: es un decorador que define el método
# que se usará
# - el parametro pasado e
@app.get(
    path='/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {
        'hello': 'world'
    }


# request and response body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person=Body(...)): # el ... significa que el parametro es obligatorio
    return person


# validaciones query parameters
@app.get(
    path='/person/detail',
    status_code=status.HTTP_200_OK
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
@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
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
    return {
        person_id: "it exists!"
    }
    

# validations: request body
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
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