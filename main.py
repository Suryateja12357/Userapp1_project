from fastapi import FastAPI
from utilities.database import engine
import models.User_model
from router import User_router
from auth import User_auth
app=FastAPI()
models.User_model.Base.metadata.create_all(bind=engine)
app.include_router(User_router.router)
app.include_router(User_auth.router)