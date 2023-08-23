from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from fastapi import APIRouter

from app.models import Note, NoteCreate, NoteUpdate
from app.database import get_session

router = APIRouter()


@router.get("/notes", response_model=list[Note])
async def get_notes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note))
    notes = result.scalars().all()
    return [
        Note(
            title=note.title,
            text=note.text,
            id=note.id,
            created_at=note.created_at,
            updated_at=note.updated_at
        ) for note in notes
    ]


@router.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    updated_views = note.views + 1
    await session.execute(update(Note).where(Note.id == note_id).values(views=updated_views))
    await session.commit()

    return Note(
        title=note.title,
        text=note.text,
        id=note.id,
        created_at=note.created_at,
        updated_at=note.updated_at
    )

@router.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: int, updated_note: NoteUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = updated_note.title
    note.text = updated_note.text
    await session.commit()

    return note

@router.post("/notes")
async def add_note(note: NoteCreate, session: AsyncSession = Depends(get_session)):
    note = Note(
        title=note.title,
        text=note.text,
    )
    session.add(note)
    await session.commit()
    await session.refresh(note)
    return note

@router.delete("/notes/{note_id}", response_model=dict)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Note).filter(Note.id == note_id))
    note = result.scalars().first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    session.delete(note)
    await session.commit()

    return {"message": "Note deleted successfully"}

