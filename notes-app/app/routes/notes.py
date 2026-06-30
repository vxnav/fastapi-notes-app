from fastapi import APIRouter, HTTPException, Depends
from app.models import Note, NoteResponse, DeleteNote, SortField, CursorPaginationResponse, UserCreate, UserLogin, UserResponse
from app.storage import insert_note, get_note_by_id, update_note, delete_note, get_all_notes, create_user, get_user_by_id, User
from app.auth import create_token, get_current_user, authenticate_user
from app.exceptions import UsernameAlreadyExists, EmailAlreadyExists, InvalidCredentials, UserNotFound
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

router = APIRouter()

# @something -> decorator: takes the function below as in charge 
# of handling requests that go to "/" with a GET operation
# also called path operation decoration
@router.get("/")
async def root():
    return {"message":"Hello World!"}

# create note
@router.post("/notes/", 
        response_model=NoteResponse, 
        response_model_exclude_none=True, 
        status_code=201)
def create_note_route(note: Note, current_user: User=Depends(get_current_user)):
    note_id = insert_note(note.title, note.content, current_user.id)
    if note_id:
        return get_note_by_id(note_id, current_user.id)
    raise HTTPException(500, "Note creation failed!")

# read note
@router.get("/notes/{note_id}", 
            response_model=NoteResponse,
            response_model_exclude_none=True)
def get_note(note_id: int, current_user=Depends(get_current_user)):
    note_row = get_note_by_id(note_id, current_user.id)
    if note_row:
        return note_row
    raise HTTPException(404, "Note not found!")


# update note
@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note_route(note_id: int, note: Note, current_user=Depends(get_current_user)):
    existing_note = get_note_by_id(note_id, current_user.id)
    if existing_note:
        update_note(note_id, current_user.id, note.title, note.content)
        return get_note_by_id(note_id, current_user.id)
    raise HTTPException(404, "Note not found!")

# delete note
@router.delete("/notes/{note_id}", 
               response_model=DeleteNote,
               response_model_exclude_none=True)
def delete_note_route(note_id: int, current_user=Depends(get_current_user)):
    deleted_note = delete_note(note_id, current_user.id)
    if deleted_note:
        return {"message": "Note deleted successfully!", "note": deleted_note}
    raise HTTPException(404, "Note not found!")

# read all notes
@router.get("/notes",
            response_model=CursorPaginationResponse,
            response_model_exclude_none=True)
def get_all_notes_route(current_user=Depends(get_current_user),
        search: str | None=None, sort: SortField | None=None,
        cursor_id: int | None=None, limit: int = 3
):
    notes = get_all_notes(current_user.id, search, sort, cursor_id, limit)
    if notes is None:
        raise HTTPException(500, "Failed to fetch notes!")
    return notes

# register user
@router.post("/register",response_model=UserResponse,status_code=201)
def register_user(user: UserCreate):
    try:
        created_user_id = create_user(user.username, user.email, user.password)
        if created_user_id:
            return get_user_by_id(created_user_id)
        raise HTTPException(500, "User couldn't be registered!")
    except UsernameAlreadyExists:
        raise HTTPException(409, "Username already exists!")
    except EmailAlreadyExists:
        raise HTTPException(409, "Email is already registered!")

# login user
@router.post("/login")
def login_user(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_found = authenticate_user(form.username, form.password)
    except InvalidCredentials:
        raise HTTPException(401, "Invalid username or password")
    
    token = create_token({"sub": str(user_found.id)})
    return token
    