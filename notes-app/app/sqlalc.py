from sqlalchemy import create_engine, String, Integer, DateTime, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session
from datetime import datetime

# create engine
engine = create_engine("sqlite:///notes.db")

# create Base
class Base(DeclarativeBase):
    pass

# create models
class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50),nullable=False)
    content: Mapped[str] = mapped_column(String(1000),nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updatedAt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
# create tables
Base.metadata.create_all(engine)

# create session
session = Session(engine)

# create a note
def insert_note(title: str, content: str):
    note = Note(title=title, content=content, createdAt=datetime.now())
    session.add(note)
    session.commit()
    return note.id

def get_note_by_id(note_id: int):
    note = session.get(Note, note_id)
    if note is None:
        return None
    return note

def update_note(note_id: int, title: str|None=None, content: str|None=None):
    note = session.get(Note, note_id)
    if note is None:
        return None

    if title is not None:
        note.title = title

    if content is not None:
        note.content = content

    note.updatedAt = datetime.now()
    session.commit()
    return note

def delete_note(note_id: int):
    note = session.get(Note, note_id)
    if note is None:
        return None
    session.delete(note)
    session.commit()
    return note

def get_all_notes(search: str|None=None, sort: str|None=None, limit=10, skip=0):
    stmt = select(Note)

    if search:
        stmt = stmt.where(Note.title.ilike(f"%{search}%")) 
    
    if sort:
        stmt = stmt.order_by(getattr(Note, sort).desc())

    stmt = stmt.limit(limit)
    stmt = stmt.offset(skip)

    return session.execute(stmt).scalars().all()
