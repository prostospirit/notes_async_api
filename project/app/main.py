from http.client import HTTPException

from fastapi import Depends, FastAPI
from sqlalchemy import update
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import init_db, get_session
from app.models import Note, Board
from app.auth import auth
from app.notes import notes

app = FastAPI()

app.include_router(notes.router, prefix='', tags=['notes'])
# app.include_router(auth.router, prefix="/auth", tags=["auth"]) # TODO add auth logic and user binding


@app.on_event("startup")
async def on_startup():
    await init_db()
