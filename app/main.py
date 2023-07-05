from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from email_authentication.email_authentication_router import email_authentication_router

app = FastAPI()

origins = ["http://3.37.125.157","http://localhost:8080"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(email_authentication_router)
