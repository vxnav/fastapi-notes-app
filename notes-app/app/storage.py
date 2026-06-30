from sqlalchemy import create_engine, String, Integer, DateTime, select, or_, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import Session
from datetime import datetime
from app.security import hash_password
from app.exceptions import UsernameAlreadyExists, EmailAlreadyExists, InvalidCredentials, UserNotFound

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
    # foreign key dependency (parent table)
    users: Mapped[list["User"]] = relationship(back_populates="notes")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String(50),nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(120),nullable=False)
    # dependency (child table)
    notes: Mapped[list["Note"]] = relationship(back_populates="users")

# create tables
Base.metadata.create_all(engine)

# create session
session = Session(engine)

# create a note
def insert_note(title: str, content: str, user_id: int):
    note = Note(title=title, content=content, createdAt=datetime.now(), user_id=user_id)
    session.add(note)
    session.commit()
    return note.id

def get_note_by_id(note_id: int, user_id: int):
    print("User ID: ",user_id)
    note = session.scalar(
        select(Note).where(Note.id==note_id, Note.user_id==user_id)
    )
    if note is None:
        return None
    return note

def update_note(note_id: int, user_id: int, title: str|None=None, content: str|None=None):
    note = session.scalar(
        select(Note).where(Note.id==note_id, Note.user_id==user_id)
    )
    if note is None:
        return None

    if title is not None:
        note.title = title

    if content is not None:
        note.content = content

    note.updatedAt = datetime.now()
    session.commit()
    return note

def delete_note(note_id: int, user_id: int):
    note = session.scalar(
        select(Note).where(Note.id==note_id, Note.user_id==user_id)
    )
    if note is None:
        return None
    session.delete(note)
    session.commit()
    return note

def get_all_notes(user_id: int,
        search: str | None=None, sort: str | None=None,
        cursor_id: int | None=None, limit: int = 3):
    stmt = select(Note).where(Note.user_id==user_id).order_by(Note.id.desc())

    if cursor_id is not None:
        stmt = stmt.where(Note.id <= cursor_id)

    if search: 
        stmt = stmt.where(
            or_(
                Note.title.ilike(f"%{search}%"), 
                Note.content.ilike(f"%{search}%")
            )
        )

    if sort:
        stmt = stmt.order_by(getattr(Note, sort).desc())

    stmt = stmt.limit(limit+1)
    notes = session.execute(stmt).scalars().all()

    has_next = False
    if len(notes)>limit:
        has_next = True
        cursor_id = notes[-1].id
        notes = notes[:-1]
    else:
        cursor_id = None

    return {
        "data": notes,
        "has_next": has_next,
        "cursor_id": cursor_id
    }

def create_user(username: str, email: str, password: str):
    # username already exists
    if session.scalar(
        select(User).where(User.username==username)
    ):
        raise UsernameAlreadyExists
    
    # if mail already exists
    if session.scalar(
        select(User).where(User.email==email)
    ):
        raise EmailAlreadyExists
    
    # hash the password
    hashed_pass = hash_password(password)

    user = User(username=username,email=email,hashed_password=hashed_pass)
    
    # add to db
    session.add(user)
    session.commit()
    return user.id

def get_user_by_name(username: str):
    user = session.scalar(
        select(User).where(User.username==username)
    )
    if user is None:
        # invalid username or password
        raise InvalidCredentials
    return user


def get_user_by_id(id: int):
    user = session.get(User, id)
    if user is None:
        # user not found
        raise UserNotFound
    return user  

    