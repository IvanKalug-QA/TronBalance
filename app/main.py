from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api.router import main_router


app = FastAPI()
add_pagination(app)

app.include_router(main_router)
