from datetime import datetime

from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    title: str
    text: str


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    pass


class Note(NoteBase, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str = Field(default=None, index=True)
    text: str = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    views: int = Field(default=0)


class Board(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
