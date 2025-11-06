from fastapi import FastAPI,HTTPException
from models.Model import Meals,UpdateMeals,User
from config.db import Database
from config.job import Job
from contextlib import asynccontextmanager
from bson.objectid import ObjectId
from routes.auth import  auth as auth_router
from routes.meals import meals_router as meals_router
import logging

@asynccontextmanager
async def lifespan(app:FastAPI):
    Database.db_connect()
    Job.start_jobs()
    yield
    Database.db_close()
app=FastAPI(lifespan=lifespan,title="tracking meals")

app.include_router(auth_router)
app.include_router(meals_router)



