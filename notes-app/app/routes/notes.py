import sqlite3
from fastapi import APIRouter, HTTPException, Query
from app.models import Note, NoteResponse, DeleteNote, SortField
from app.storage import insert_note, get_note_by_id, update_note, delete_note, get_all_notes
from datetime import datetime
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
def create_note_route(note: Note):
    note_id = insert_note((note.title, note.content, datetime.now()))
    if note_id:
        return get_note_by_id(note_id)
    raise HTTPException(500, "Note creation failed!")

# read note
@router.get("/notes/{note_id}", 
            response_model=NoteResponse,
            response_model_exclude_none=True)
def get_note(note_id: int):
    note_row = get_note_by_id(note_id)
    if note_row:
        return note_row
    raise HTTPException(404, "Note not found!")


# update note
@router.put("/notes/{note_id}", response_model=NoteResponse)
def update_note_route(note_id: int, note: Note):
    existing_note = get_note_by_id(note_id)
    if existing_note:
        update_note((note.title, note.content, datetime.now(), note_id))
        return get_note_by_id(note_id)
    raise HTTPException(404, "Note not found!")

# delete note
@router.delete("/notes/{note_id}", 
               response_model=DeleteNote,
               response_model_exclude_none=True)
def delete_note_route(note_id: int):
    deleted_note = delete_note(note_id)
    if deleted_note:
        return {"message": "Note deleted successfully!", "note": deleted_note}
    raise HTTPException(404, "Note not found!")

# read all notes
@router.get("/notes", 
         response_model=list[NoteResponse],
         response_model_exclude_none=True)
def get_all_notes_route(
    search: str | None = None,
    sort: SortField | None = None,
    limit: Annotated[int, Query(gt=0, lt=100)] = 10,
    skip: Annotated[int, Query(ge=0)] = 0
):
    notes = get_all_notes(search, sort.value if sort else None, limit, skip)
    if notes is None:
        raise HTTPException(500, "Failed to fetch notes!")
    return notes
