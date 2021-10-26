""" API entrypoint """
# python
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List
import json
# pydantic
from pydantic import BaseModel
from pydantic import EmailStr, Field
# fastapi
from fastapi import FastAPI, status, Query, Body


app = FastAPI()

# models
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)
    
class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(..., min_length=1, max_length=256)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

# Path Operations


## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="register a user",
    tags=['users',]
)
def signup(user: UserRegister = Body(...)):
    """ 
    # Signup
    This Path operation register a user in the app
    
    parameters:
    - Request Body parameter
        - user: UserRegister
        
    return a json with the basic user information:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open(file='users.json', mode='r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        
        user_dict = user.dict()
        user_dict['user_id'] = str(user_dict['user_id'])
        user_dict['birth_date'] = str(user_dict['birth_date'])
        
        results.append(user_dict)
        
        f.seek(0)
        f.write(json.dumps(results))
    
    return user_dict

### Login an user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="login a user",
    tags=['users',]
)
def login():
    pass

### show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=['users',]
)
def show_all_users():
    """
    # Show all users
    
    This path operation shows all users in the app
    
    Parameters:
    - None
    
    Return a json list with all users in the app, with the following parameters:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_date: date
    """
    with open(file='users.json', mode='r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        return results

### Show an user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=['users',]
)
def show_a_user(user_id: str = Query(...)):
    pass

### Delete an user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=['users',]
)
def delete_a_user(user_id: str = Query(...)):
    pass

### Update an user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=['users',]
)
def update_a_user(user_id: str = Query(...)):
    pass

## Tweets

### Show all tweets
@app.get(
    path='/',
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary='Show all tweets',
    tags=['tweets',]
)
def show_all_tweets():
    """ 
    # Show all tweets
    
    Show all tweets in the app
    
    parameters:
    - None
        
    return a json list with the tweets information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open(file='tweets.json', mode='r+', encoding='utf-8') as f:
        return json.loads(f.read())

### Post a Tweet
@app.post(
    path='/post',
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary='Post a tweet',
    tags=['tweets',]
)
def post_tweet(tweet: Tweet = Body(...)):
    """ 
    # Post a tweet
    POst a tweet in the app
    
    parameters:
    - Request Body parameter
        - tweet: Tweet
        
    return a json with the basic tweet information:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open(file='tweets.json', mode='r+', encoding='utf-8') as f:
        results = json.loads(f.read())
        
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict['updated_at'])
        
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])
        results.append(tweet_dict)
        
        f.seek(0)
        f.write(json.dumps(results))
    
    return tweet_dict

### Show a Tweet
@app.get(
    path='/tweets/{tweet_id}',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Show a tweet',
    tags=['tweets',]
)
def show_tweet():
    pass

### delete a tweet
@app.delete(
    path='/tweets/{tweet_id}/delete',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Delete a tweet',
    tags=['tweets',]
)
def delete_tweet():
    pass

### update a tweet
@app.delete(
    path='/tweets/{tweet_id}/update',
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary='Update a tweet',
    tags=['tweets',]
)
def update_tweet():
    pass