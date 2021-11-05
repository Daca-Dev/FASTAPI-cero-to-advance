# python
from typing import Optional
from pathlib import Path
# fastapi
from fastapi import (
    FastAPI, Depends, Cookie, Header,
    HTTPException, status
)
from fastapi.responses import (
    RedirectResponse, FileResponse
)


app = FastAPI()
# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])

# fake db
fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


# dependencies
# functions
# <- params exactly the same like a path opertaion
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {
        "q": q,
        "skip": skip,
        "limit": limit
    }
# objects


class CommonQueryParams:
    # <- params exactly the same like a path opertaion
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get(
    path='/'
)
def home():
    return {
        'message': 'Hello World!'
    }


# path operation with a dependency

# (function)
@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

# (function)


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

# (clases)
@app.get('/teams/')
async def read_teams(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items": items})
    return response


# sub-dependecy
def query_extractor(q: Optional[str] = None):
    return q

# dependecy
def query_or_cookie_extractor(
    q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)
):
    if not q:
        return last_query
    return q

# Path operation
@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}

########################
# Decorator dependencies

# dependencies
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

# path operations
@app.get("/items-decoration/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

# redirection
@app.get('/redirect')
async def redirect():
    return RedirectResponse('items')


# response with a file
@app.get("/cat")
async def get_cat():
    root_directory = Path('.')
    picture_path = root_directory / "images/cat.jpg"
    return FileResponse(picture_path)