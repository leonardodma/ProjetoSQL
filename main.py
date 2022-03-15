from fastapi import FastAPI, Query, Path, Body, Header
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime, time, timedelta
from uuid import UUID

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Bem-vindo ao seu mercado!"}


